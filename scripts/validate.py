#!/usr/bin/env python3
"""Check community content offline. Run from any directory with Python 3.10+."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

try:
    from markdown_it import MarkdownIt
    import yaml
except ImportError:
    sys.exit("Install dependencies first: python -m pip install -r requirements-dev.txt")

ROOT = Path(__file__).resolve().parents[1]
MAX_IMAGE_BYTES = 1_572_864  # 1.5 MiB per image; keep the public profile quick to load.
IMAGE_SUFFIXES = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"}
SKIP_DIRS = {".git", ".venv", "__pycache__"}
MARKDOWN = MarkdownIt("commonmark").enable("table")
ERRORS = []


def error(path, message):
    ERRORS.append(f"{path.relative_to(ROOT)}: {message}")


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def slug(text):
    """GitHub-style heading IDs, including repeated headings and Unicode text."""
    text = text.lower()
    text = "".join(c for c in text if c in "-_" or not unicodedata.category(c).startswith(("P", "S", "C")))
    return text.replace(" ", "-")


class Document(HTMLParser):
    def __init__(self, path, source):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links = []
        self.anchors = set()
        self.counts = Counter()
        self.heading = None
        self.feed(MARKDOWN.render(source))
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.anchors.add(attrs["id"])
        if tag == "a":
            if attrs.get("name"):
                self.anchors.add(attrs["name"])
            if attrs.get("href"):
                self.links.append((attrs["href"], False))
        if re.fullmatch(r"h[1-6]", tag):
            self.heading = []
        if tag == "img":
            if not nonempty(attrs.get("alt")):
                error(self.path, "image needs descriptive alt text")
            if not nonempty(attrs.get("src")):
                error(self.path, "image needs a src URL")
            else:
                self.links.append((attrs["src"], True))
            if self.heading is not None:
                self.heading.append(attrs.get("alt", ""))
        if tag in {"img", "source"} and attrs.get("srcset"):
            for candidate in attrs["srcset"].split(","):
                if candidate.strip():
                    self.links.append((candidate.strip().split()[0], True))

    def handle_data(self, data):
        if self.heading is not None:
            self.heading.append(data)

    def handle_endtag(self, tag):
        if re.fullmatch(r"h[1-6]", tag) and self.heading is not None:
            base = slug("".join(self.heading))
            anchor = base
            while anchor in self.anchors:
                self.counts[base] += 1
                anchor = f"{base}-{self.counts[base]}"
            self.anchors.add(anchor)
            self.heading = None


def local_target(source, url):
    """Map relative links and this repository's public main URLs to local paths."""
    parsed = urlsplit(url)
    path = unquote(parsed.path)
    if parsed.netloc:
        prefixes = {
            "raw.githubusercontent.com": ("/quirq-ai/.github/main/", "/quirq-ai/.github/refs/heads/main/"),
            "github.com": ("/quirq-ai/.github/blob/main/", "/quirq-ai/.github/tree/main/"),
        }
        prefix = next((p for p in prefixes.get(parsed.netloc.lower(), ()) if path.startswith(p)), None)
        if prefix is None:
            return None
        target = ROOT / path[len(prefix):]
    elif parsed.scheme:
        if parsed.scheme not in {"https", "http", "mailto"}:
            error(source, f"unsupported link scheme: {url}")
        return None
    else:
        target = (ROOT / path.lstrip("/")) if path.startswith("/") else (source.parent / path if path else source)
    target = target.resolve()
    if not target.is_relative_to(ROOT):
        error(source, f"link escapes repository: {url}")
        return None
    return target, unquote(parsed.fragment)


def check_links(document, documents):
    for url, image in document.links:
        result = local_target(document.path, url)
        if result is None:
            continue  # External availability is reviewed separately, without network-dependent CI.
        target, fragment = result
        if not target.exists():
            error(document.path, f"missing local target: {url}")
        elif image and not target.is_file():
            error(document.path, f"image target is not a file: {url}")
        elif fragment and target.suffix.lower() == ".md":
            if target not in documents:
                error(document.path, f"Markdown target was not scanned: {url}")
            elif fragment.removeprefix("user-content-") not in documents[target].anchors:
                error(document.path, f"missing heading or HTML anchor: {url}")


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys; preserve YAML 1.2 keys such as Actions' `on`."""


UniqueLoader.yaml_implicit_resolvers = {
    key: [(tag, pattern) for tag, pattern in resolvers if tag != "tag:yaml.org,2002:bool"]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
UniqueLoader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|false)$", re.I), list("tTfF"))


def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, (str, int, float, bool, type(None))):
            raise yaml.constructor.ConstructorError(None, None, "mapping keys must be scalar", key_node.start_mark)
        if key in result:
            raise yaml.constructor.ConstructorError(None, None, f"duplicate key: {key}", key_node.start_mark)
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def check_issue_config(path, data):
    if "blank_issues_enabled" in data and not isinstance(data["blank_issues_enabled"], bool):
        error(path, "blank_issues_enabled must be true or false")
    contacts = data.get("contact_links", [])
    if not isinstance(contacts, list):
        error(path, "contact_links must be a list")
        return
    for index, contact in enumerate(contacts, 1):
        if not isinstance(contact, dict) or any(not nonempty(contact.get(k)) for k in ("name", "url", "about")):
            error(path, f"contact link {index} needs name, url and about")
        elif urlsplit(contact["url"]).scheme not in {"https", "mailto"}:
            error(path, f"contact link {index} needs an HTTPS or mailto URL")


def check_issue_form(path, data):
    for key in ("name", "description"):
        if not nonempty(data.get(key)):
            error(path, f"issue form needs a nonempty {key}")
    body = data.get("body")
    if not isinstance(body, list) or not body:
        error(path, "issue form needs a nonempty body list")
        return
    ids = set()
    input_count = 0
    for index, field in enumerate(body, 1):
        where = f"body item {index}"
        if not isinstance(field, dict):
            error(path, f"{where} must be a mapping")
            continue
        kind = field.get("type")
        attrs = field.get("attributes")
        if kind not in {"markdown", "input", "textarea", "dropdown", "checkboxes", "upload"}:
            error(path, f"{where} has unsupported type: {kind}")
        if not isinstance(attrs, dict):
            error(path, f"{where} needs attributes")
            continue
        if kind == "markdown":
            if not nonempty(attrs.get("value")):
                error(path, f"{where} needs a Markdown value")
            continue
        input_count += 1
        field_id = field.get("id")
        if not nonempty(field_id) or not re.fullmatch(r"[A-Za-z0-9_-]+", field_id):
            error(path, f"{where} needs an alphanumeric id (hyphens and underscores allowed)")
        elif field_id in ids:
            error(path, f"duplicate field id: {field_id}")
        else:
            ids.add(field_id)
        if not nonempty(attrs.get("label")):
            error(path, f"{where} needs a label")
        validations = field.get("validations", {})
        if not isinstance(validations, dict) or ("required" in validations and not isinstance(validations["required"], bool)):
            error(path, f"{where} validations.required must be true or false")
        if kind in {"dropdown", "checkboxes"}:
            options = attrs.get("options")
            if not isinstance(options, list) or not options:
                error(path, f"{where} needs a nonempty options list")
            elif kind == "dropdown" and any(not nonempty(o) for o in options):
                error(path, f"{where} dropdown options must be strings")
            elif kind == "checkboxes" and any(not isinstance(o, dict) or not nonempty(o.get("label")) for o in options):
                error(path, f"{where} checkbox options need labels")
    if not input_count:
        error(path, "issue form needs at least one input field")


def check_yaml(path):
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    except (yaml.YAMLError, UnicodeError) as exc:
        error(path, f"invalid YAML: {exc}")
        return
    if not isinstance(data, dict):
        error(path, "YAML document must be a mapping")
        return
    if path.parent.name == "ISSUE_TEMPLATE":
        (check_issue_config if path.stem == "config" else check_issue_form)(path, data)
    elif path.parent.name == "workflows":
        if not data.get("on") or not isinstance(data.get("jobs"), dict) or not data["jobs"]:
            error(path, "workflow needs triggers (on) and at least one job")


def main():
    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and not SKIP_DIRS.intersection(p.relative_to(ROOT).parts))
    documents = {}
    yaml_count = 0
    image_count = 0
    for path in files:
        suffix = path.suffix.lower()
        if suffix == ".md":
            documents[path] = Document(path, path.read_text(encoding="utf-8"))
        elif suffix in {".yaml", ".yml"}:
            check_yaml(path)
            yaml_count += 1
        elif suffix in IMAGE_SUFFIXES:
            image_count += 1
            if path.stat().st_size > MAX_IMAGE_BYTES:
                error(path, f"image exceeds {MAX_IMAGE_BYTES:,} bytes; resize or compress it")
    for document in documents.values():
        check_links(document, documents)
    if ERRORS:
        print("Content validation failed:", file=sys.stderr)
        for message in ERRORS:
            print(f"  - {message}", file=sys.stderr)
        return 1
    print(f"Validated {len(documents)} Markdown files, {yaml_count} YAML files and {image_count} images. External URLs were not fetched.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
