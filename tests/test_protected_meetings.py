"""Security regression checks; run: python -m unittest discover -s tests -v."""
import base64
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "build_protected_meetings.py"
spec = importlib.util.spec_from_file_location("meeting_builder", MODULE)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def metadata(page):
    return json.loads(re.search(r"const encryptedNote = (\{.*?\});", page).group(1))


def decrypt(data, password):
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), base64.b64decode(data["salt"]), data["iterations"], dklen=32)
    return AESGCM(key).decrypt(base64.b64decode(data["iv"]), base64.b64decode(data["ciphertext"]), b"csdi-meeting-v1").decode()


class ProtectedMeetingTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        sources = self.root / "meetings"
        sources.mkdir()
        media = sources / "assets"
        media.mkdir()
        public = self.root / "docs"
        replacements = dict(REPO=self.root, SOURCES=sources, MEETING_MEDIA=media,
                            PUBLIC=public, PUBLIC_NOTES=public / "meetings", DATA=public / "_data")
        patches = patch.multiple(builder, **replacements)
        patches.start()
        self.addCleanup(patches.stop)

    def note(self, contents, name="2026-10-21.rst"):
        path = builder.SOURCES / name
        path.write_text(contents, encoding="utf-8")
        return path

    def test_authenticated_encryption_and_wrong_password(self):
        plaintext = "PRIVATE_AUDIT_MARKER_7283"
        password = "disposable-audit-password-7283"
        page = builder.encrypted_page("2026-10-21", plaintext, password)
        self.assertNotIn(plaintext, page)
        self.assertNotIn(password, page)
        data = metadata(page)
        self.assertEqual(plaintext, decrypt(data, password))
        with self.assertRaises(InvalidTag):
            decrypt(data, "wrong-password")
        damaged = bytearray(base64.b64decode(data["ciphertext"]))
        damaged[0] ^= 1
        data["ciphertext"] = base64.b64encode(damaged).decode()
        with self.assertRaises(InvalidTag):
            decrypt(data, password)

    def test_each_encryption_has_fresh_salt_and_nonce(self):
        first = metadata(builder.encrypted_page("2026-10-21", "same note", "password"))
        second = metadata(builder.encrypted_page("2026-10-21", "same note", "password"))
        self.assertNotEqual(first["salt"], second["salt"])
        self.assertNotEqual(first["iv"], second["iv"])
        self.assertEqual(len(base64.b64decode(first["salt"])), 16)
        self.assertEqual(len(base64.b64decode(first["iv"])), 12)

    def test_images_are_embedded_inside_encryption(self):
        image = b"\x89PNG\r\n\x1a\nprivate-sample-image"
        (builder.MEETING_MEDIA / "result.png").write_bytes(image)
        note = self.note("Meeting\n=======\n\n.. image:: assets/result.png\n   :alt: Result plot\n")
        rendered = builder.render_rst(note)
        encoded = base64.b64encode(image).decode()
        self.assertIn("data:image/png;base64," + encoded, rendered)
        page = builder.encrypted_page(note.stem, rendered, "audit-password")
        self.assertNotIn(encoded, page)
        self.assertNotIn("assets/result.png", page)

    def test_external_and_escaping_image_paths_are_rejected(self):
        note = self.note("Meeting\n=======\n")
        for src in ["https://example.com/private.png", "//example.com/x.png", "../secret.png", "assets/%2e%2e/%2e%2e/secret.png", "assets/x.png?token=private", "data:image/png;base64,AA=="]:
            with self.subTest(src=src), self.assertRaises(ValueError):
                builder.encrypted_image_uri(note, src)

    def test_oversized_image_is_rejected_before_reading(self):
        note = self.note("Meeting\n=======\n")
        image = builder.MEETING_MEDIA / "large.png"
        with image.open("wb") as stream:
            stream.seek(builder.MAX_IMAGE_BYTES)
            stream.write(b"0")
        with self.assertRaisesRegex(ValueError, "larger than"):
            builder.encrypted_image_uri(note, "assets/large.png")

    def test_raw_and_include_directives_fail_without_logging_source(self):
        for directive in [".. raw:: html\n\n   <script>PRIVATE_AUDIT_MARKER</script>\n", ".. include:: PRIVATE_AUDIT_MARKER\n"]:
            with self.subTest(directive=directive):
                note = self.note(directive)
                errors = io.StringIO()
                with contextlib.redirect_stderr(errors), self.assertRaises(ValueError) as result:
                    builder.render_rst(note)
                self.assertNotIn("PRIVATE_AUDIT_MARKER", errors.getvalue())
                self.assertNotIn("PRIVATE_AUDIT_MARKER", str(result.exception))

    def test_equations_render_without_warnings(self):
        note = self.note("Meeting\n=======\n\nInline :math:`x^2` and a block:\n\n.. math::\n\n   y = x^2\n")
        rendered = builder.render_rst(note)
        self.assertIn("x^2", rendered)
        self.assertNotIn("system-message", rendered)

    def test_missing_password_writes_nothing(self):
        with patch.dict(os.environ, {"MEETING_PASSWORD": ""}), self.assertRaises(SystemExit):
            builder.main()
        self.assertFalse(builder.PUBLIC.exists())

    def test_invalid_date_prevents_output(self):
        self.note("Meeting\n=======\n", "2026-02-31.rst")
        with patch.dict(os.environ, {"MEETING_PASSWORD": "audit-password"}), self.assertRaises(SystemExit):
            builder.main()
        self.assertEqual(list(builder.PUBLIC_NOTES.glob("*.html")), [])

    def test_build_writes_only_encrypted_pages_and_dates(self):
        self.note("Meeting\n=======\n\nPRIVATE_AUDIT_MARKER_7283\n")
        with patch.dict(os.environ, {"MEETING_PASSWORD": "audit-password"}), contextlib.redirect_stdout(io.StringIO()):
            builder.main()
        files = list(builder.PUBLIC.rglob("*"))
        files = [x for x in files if x.is_file()]
        self.assertEqual({x.name for x in files}, {"2026-10-21.html", "meetings.json"})
        for output in files:
            self.assertNotIn("PRIVATE_AUDIT_MARKER_7283", output.read_text())
        self.assertEqual(json.loads((builder.DATA / "meetings.json").read_text()), ["2026-10-21"])


if __name__ == "__main__":
    unittest.main()
