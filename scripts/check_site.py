"""Validate the docs-only Pages artifact before publishing (standard library only)."""
from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit


class Document(HTMLParser):
    def __init__(self, text: str) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.feed(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get('id'):
            self.ids.add(values['id'])
        key = {'a': 'href', 'img': 'src', 'link': 'href', 'script': 'src'}.get(tag)
        if key and values.get(key):
            self.links.append(values[key])


def check_site(directory: Path, origin: str, baseurl: str) -> None:
    directory = directory.resolve()
    prefix = baseurl.rstrip('/')
    host = urlsplit(origin).netloc
    errors: list[str] = []
    docs = {p: Document(p.read_text(encoding='utf-8')) for p in directory.rglob('*.html')}
    for name in ['index.html', 'meetings/index.html', 'assets/style.css', 'assets/webfonts/fa-solid-900.woff2']:
        if not (directory / name).is_file():
            errors.append('Missing public file: ' + name)
    for p in directory.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(directory).as_posix()
        if p.suffix.lower() in {'.rst', '.py', '.pyc', '.yml', '.yaml'} or p.name in {'README.md', 'README.html', '.DS_Store'}:
            errors.append('Source file in public artifact: ' + rel)
        if rel.startswith(('meetings/assets/', '.git/', 'research/', 'scripts/', '_templates/')):
            errors.append('Private or build directory in public artifact: ' + rel)
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}\.html', p.name) and p.parent == directory / 'meetings':
            text = p.read_text(encoding='utf-8')
            match = re.search(r'const encryptedNote = (\{[^\n]+\});', text)
            try:
                payload = json.loads(match[1]) if match else {}
                assert all(payload.get(key) for key in ['salt', 'iv', 'ciphertext', 'iterations'])
                dt.date.fromisoformat(p.stem)
            except (ValueError, AssertionError):
                errors.append('Meeting page is not encrypted: ' + rel)
    checked = 0
    for p, doc in docs.items():
        route = prefix + '/' + p.relative_to(directory).as_posix()
        for value in doc.links:
            if not value or value.startswith(('data:', 'mailto:', 'tel:', 'javascript:')):
                continue
            target = urlsplit(urljoin(origin + route, value))
            if target.scheme not in {'http', 'https'} or target.netloc != host:
                continue
            path = unquote(target.path)
            if prefix and path != prefix and not path.startswith(prefix + '/'):
                errors.append(f'{p.name}: link misses repository path: {value}')
                continue
            relative = path[len(prefix):].lstrip('/')
            candidate = (directory / relative).resolve()
            if not candidate.is_relative_to(directory):
                errors.append(f'{p.name}: link escapes public directory: {value}')
                continue
            if candidate.is_dir() or path.endswith('/'):
                candidate /= 'index.html'
            elif not candidate.is_file() and not candidate.suffix:
                candidate = candidate.with_suffix('.html')
            if not candidate.is_file():
                errors.append(f'{p.name}: missing link target: {value}')
            elif target.fragment and candidate in docs and unquote(target.fragment) not in docs[candidate].ids:
                errors.append(f'{p.name}: missing link anchor: {value}')
            checked += 1
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Validated {len(docs)} HTML pages, {checked} local links, encrypted meeting pages, and public artifact boundaries.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--url', default='https://hendrisutrisno.github.io')
    parser.add_argument('--baseurl', default='/2026student')
    args = parser.parse_args()
    check_site(args.directory, args.url.rstrip('/'), args.baseurl)
