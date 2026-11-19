#!/usr/bin/env python3
"""Register the Claudeaux GitHub App from app/manifest.json.

Serves a one-button form on localhost that submits the manifest to
GitHub's create-from-manifest flow, catches the redirect carrying the
conversion code, exchanges it, and stores the resulting credentials:

    ~/.config/claudeaux/<slug>.json   (app id, slug, owner)
    ~/.config/claudeaux/<slug>.pem    (private key, chmod 600)

Usage:
    register-app.py              # register under your user account
    register-app.py --org ORG    # register under an org you own
"""

import argparse
import http.server
import json
import pathlib
import secrets
import sys
import urllib.request
import webbrowser

CONFIG_DIR = pathlib.Path.home() / ".config" / "claudeaux"
PORT = 8713


def main() -> int:
    """Run the registration flow."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--org", help="organization to own the app")
    args = parser.parse_args()

    manifest_path = pathlib.Path(__file__).parent.parent / "app" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["redirect_url"] = f"http://localhost:{PORT}/callback"

    target = (
        f"https://github.com/organizations/{args.org}/settings/apps/new"
        if args.org
        else "https://github.com/settings/apps/new"
    )
    state = secrets.token_urlsafe(16)
    form = f"""<!DOCTYPE html>
<html><body>
<form action="{target}?state={state}" method="post">
  <input type="hidden" name="manifest" value='{json.dumps(manifest)}'>
  <button type="submit" style="font-size:2em">Create the Claudeaux app</button>
</form>
</body></html>"""

    result: dict = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            if self.path.startswith("/callback"):
                from urllib.parse import parse_qs, urlparse

                query = parse_qs(urlparse(self.path).query)
                if query.get("state", [""])[0] != state:
                    self.send_error(400, "state mismatch")
                    return
                result["code"] = query["code"][0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Claudeaux is registered. You can close this tab.")
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(form.encode())

        def log_message(self, *_):
            pass

    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Open http://localhost:{PORT}/ and click the button...")
    webbrowser.open(f"http://localhost:{PORT}/")
    while "code" not in result:
        server.handle_request()

    request = urllib.request.Request(
        f"https://api.github.com/app-manifests/{result['code']}/conversions",
        method="POST",
        headers={"Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(request) as response:
        app = json.load(response)

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    slug = app["slug"]
    pem_path = CONFIG_DIR / f"{slug}.pem"
    pem_path.write_text(app["pem"])
    pem_path.chmod(0o600)
    meta = {
        "app_id": app["id"],
        "slug": slug,
        "owner": app["owner"]["login"],
        "html_url": app["html_url"],
    }
    (CONFIG_DIR / f"{slug}.json").write_text(json.dumps(meta, indent=2) + "\n")

    print(f"Registered {slug} (app id {app['id']}) owned by {meta['owner']}")
    print(f"Credentials: {CONFIG_DIR}/{slug}.json + {slug}.pem (0600)")
    print(f"Install it:  {app['html_url']}/installations/new")
    return 0


if __name__ == "__main__":
    sys.exit(main())
