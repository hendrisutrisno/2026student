#!/usr/bin/env python3
"""Build AES-GCM encrypted GitHub Pages HTML from private root meetings/*.rst.

The source notes remain outside docs/, so GitHub Pages publishes only encrypted HTML.
MEETING_PASSWORD must be set as a GitHub Actions repository secret.
"""

from __future__ import annotations

import base64
import datetime as dt
import hashlib
import html
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

REPO = Path(__file__).resolve().parents[1]
SOURCES = REPO / "meetings"
PUBLIC = REPO / "docs"
PUBLIC_NOTES = PUBLIC / "meetings"
DATA = PUBLIC / "_data"
ITERATIONS = 310_000
AAD = b"csdi-meeting-v1"
DATE_NAME = re.compile(r"\d{4}-\d{2}-\d{2}\.rst\Z")
HTML_NAME = re.compile(r"\d{4}-\d{2}-\d{2}\.html\Z")
THEME_BOOTSTRAP = '''<script>
(function() {
  var saved = localStorage.getItem("theme");
  var prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  document.documentElement.setAttribute("data-theme", saved || (prefersDark ? "dark" : "light"));
})();
</script>'''
THEME_TOGGLE = '''<script>
(function() {
  var button = document.getElementById("theme-toggle");
  if (!button) return;
  button.addEventListener("click", function() {
    var current = document.documentElement.getAttribute("data-theme");
    var next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  });
})();
</script>'''


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def render_rst(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    try:
        from docutils.core import publish_parts
    except ImportError:
        # Convenient for local preview where pandoc is already installed.
        if not __import__("shutil").which("pandoc"):
            raise SystemExit("Install docutils: python -m pip install docutils")
        return subprocess.check_output(
            ["pandoc", "--from=rst", "--to=html", "--standalone=false"],
            input=text.encode("utf-8"),
        ).decode("utf-8")
    parts = publish_parts(
        source=text,
        writer_name="html5",
        settings_overrides={
            "raw_enabled": False,
            "file_insertion_enabled": False,
            "report_level": 4,
            "halt_level": 6,
            "syntax_highlight": "none",
        },
    )
    return parts["html_body"]


def note_document(label: str, inner: str) -> str:
    title = html.escape(f"Regular Meeting - {label}")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>{title} | CSDI Lab</title>
  {THEME_BOOTSTRAP}
  <link rel="stylesheet" href="../assets/style.css">
  <style>
    .note-body {{max-width:820px;margin:0 auto;line-height:1.7}}
    .note-toolbar {{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-bottom:28px}}
    .note-toolbar p {{margin:0}}
    .note-body h1 {{font-size:2rem;letter-spacing:-.02em}}
    .note-body h2 {{font-size:1.35rem;margin-top:2em}}
    .note-body pre {{overflow-x:auto;background:var(--surface-2);border:1px solid var(--border);padding:1rem;border-radius:8px}}
    .note-body img {{max-width:100%}}
    .note-body table {{display:block;overflow-x:auto}}
  </style>
</head>
<body>
  <main class="shell note-body" style="padding-top:38px;padding-bottom:75px">
    <div class="note-toolbar">
      <p><a href="./">&larr; Regular meetings</a> &middot; <a href="../">Research journey</a></p>
      <button class="theme-toggle" id="theme-toggle" aria-label="Toggle dark/light mode" title="Toggle theme"><i class="theme-icon" aria-hidden="true"></i></button>
    </div>
    {inner}
  </main>
  {THEME_TOGGLE}
</body>
</html>'''


def encrypted_page(label: str, plaintext: str, password: str) -> str:
    salt = secrets.token_bytes(16)
    iv = secrets.token_bytes(12)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS, dklen=32)
    encrypted = AESGCM(key).encrypt(iv, plaintext.encode("utf-8"), AAD)
    metadata = json.dumps(
        {"salt": b64(salt), "iv": b64(iv), "ciphertext": b64(encrypted), "iterations": ITERATIONS},
        separators=(",", ":"),
    ).replace("<", "\\u003c")
    title = html.escape(f"Regular Meeting - {label}")
    # The password is NOT embedded in this HTML. Only salt, nonce and ciphertext are public.
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>{title} | Protected Research Check-in</title>
  {THEME_BOOTSTRAP}
  <link rel="stylesheet" href="../assets/style.css">
  <style>
    * {{box-sizing:border-box}}
    body {{min-height:100vh;margin:0;display:grid;place-items:center;padding:20px}}
    .card {{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:36px;max-width:440px;width:100%;box-shadow:0 8px 40px rgba(0,0,0,.12)}}
    .theme-control {{position:fixed;top:18px;right:20px}}
    .theme-control .theme-toggle {{margin:0}}
    .eyebrow {{font-size:12px;letter-spacing:.1em;font-weight:750;color:var(--accent)}}
    h1 {{font-size:25px;line-height:1.25;margin:16px 0 10px}}
    p {{font-size:14px;color:var(--muted);line-height:1.6;margin:0 0 20px}}
    label {{display:block;font-weight:650;font-size:14px;margin-bottom:8px}}
    input {{display:block;width:100%;border:1px solid var(--border-strong);border-radius:8px;padding:12px;font:inherit;background:var(--surface-2);color:var(--ink)}}
    input:focus {{outline:2px solid var(--accent);outline-offset:1px}}
    #button {{background:var(--accent);color:white;border:0;border-radius:8px;padding:12px 16px;font-size:15px;font-weight:700;cursor:pointer;margin-top:14px;width:100%}}
    #button:hover {{background:var(--accent-dark)}}
    #button:disabled {{opacity:.6;cursor:wait}}
    .back {{display:block;margin-top:22px;color:var(--accent);font-size:13px}}
    #error {{color:var(--error);font-size:13px;min-height:1.2em;margin-top:12px}}
  </style>
</head>
<body>
  <div class="theme-control"><button class="theme-toggle" id="theme-toggle" aria-label="Toggle dark/light mode" title="Toggle theme"><i class="theme-icon" aria-hidden="true"></i></button></div>
  <div class="card">
    <div class="eyebrow">CSDI LAB &middot; RESEARCH CHECK-IN</div>
    <h1>{title}</h1>
    <p>This meeting record is password-protected.</p>
    <form id="unlock">
      <label for="password">Meeting password</label>
      <input id="password" type="password" autocomplete="current-password" required autofocus>
      <button id="button" type="submit">Unlock meeting note</button>
      <div id="error" role="alert" aria-live="polite"></div>
    </form>
    <a class="back" href="./">&larr; Back to regular meetings</a>
  </div>
<script>
"use strict";
const encryptedNote = {metadata};
const textEncoder = new TextEncoder();
function fromB64(s) {{
  return Uint8Array.from(atob(s), c => c.charCodeAt(0));
}}
async function decryptNote(password) {{
  const baseKey = await crypto.subtle.importKey("raw", textEncoder.encode(password), "PBKDF2", false, ["deriveKey"]);
  const key = await crypto.subtle.deriveKey(
    {{name:"PBKDF2", salt:fromB64(encryptedNote.salt), iterations:encryptedNote.iterations, hash:"SHA-256"}},
    baseKey, {{name:"AES-GCM",length:256}}, false, ["decrypt"]
  );
  const data = await crypto.subtle.decrypt(
    {{name:"AES-GCM",iv:fromB64(encryptedNote.iv),additionalData:textEncoder.encode("csdi-meeting-v1")}},
    key,fromB64(encryptedNote.ciphertext)
  );
  return new TextDecoder("utf-8",{{fatal:true}}).decode(data);
}}
document.getElementById("unlock").addEventListener("submit",async function(event) {{
  event.preventDefault();
  const button=document.getElementById("button");
  const error=document.getElementById("error");
  button.disabled=true;
  error.textContent="";
  try {{
    if (!crypto.subtle) throw new Error("HTTPS required for secure decryption.");
    const contents=await decryptNote(document.getElementById("password").value);
    document.open();document.write(contents);document.close();
  }} catch (e) {{
    error.textContent=e.message.includes("HTTPS required")?e.message:"Incorrect password or unreadable note.";
    button.disabled=false;
  }}
}});
</script>
{THEME_TOGGLE}
</body>
</html>'''


def main() -> None:
    password = os.environ.get("MEETING_PASSWORD", "")
    if not password:
        raise SystemExit("Missing MEETING_PASSWORD. Set a repository secret in Settings > Secrets and variables > Actions. No pages were published.")

    PUBLIC_NOTES.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)

    paths = sorted(SOURCES.glob("*.rst")) if SOURCES.exists() else []
    dates = []
    for path in paths:
        if not DATE_NAME.fullmatch(path.name):
            raise SystemExit(f"Invalid meeting note filename: {path.name}. Use YYYY-MM-DD.rst.")
        label = path.stem
        try:
            dt.date.fromisoformat(label)
        except ValueError as exc:
            raise SystemExit(f"Invalid meeting date {label}") from exc
        dates.append(label)

    # Remove stale generated pages in CI workspace; never commit these files.
    for previous in PUBLIC_NOTES.glob("*.html"):
        if HTML_NAME.fullmatch(previous.name):
            previous.unlink()

    for path in paths:
        doc = note_document(path.stem, render_rst(path))
        locked = encrypted_page(path.stem, doc, password)
        (PUBLIC_NOTES / (path.stem + ".html")).write_text(locked, encoding="utf-8")

    (DATA / "meetings.json").write_text(json.dumps(sorted(dates, reverse=True), indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(dates)} encrypted meeting page(s) and a public dates-only index.")


if __name__ == "__main__":
    main()
