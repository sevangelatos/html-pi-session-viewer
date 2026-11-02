# pi-session-viewer

A standalone, single-file HTML viewer for [pi](https://pi.dev) session `.jsonl` files.

`/export` in pi produces an HTML page with the session data baked in. This project
produces the same viewer **without** baked-in data: open the page and drag & drop any
session `.jsonl` onto it.

## Usage

1. Open `dist/session-viewer.html` in a browser (no server, no network needed).
2. Drop a session `.jsonl` onto the page, or click **choose a file…**.
3. Drop another file at any time to switch sessions.

Everything runs locally; the file is never uploaded.

The viewer is pi's own export UI (session tree, search, filters, thinking/tool
toggles, markdown + syntax highlighting, JSONL download), so it looks and behaves
like a regular export.

## Build

Requires `python3` and `pi` on your `PATH`.

```sh
./build.py                      # runs `pi --export` on src/base-session.jsonl
./build.py some-export.html     # or reuse an existing pi-exported HTML
```

Output: `dist/session-viewer.html`. The build is tied to the installed pi version, so
rebuild after upgrading pi to pick up viewer changes. The committed `dist/` file is a
ready-to-use build.

### How it works

- `build.py` takes a pi export, replaces the embedded `<script id="session-data">`
  payload with a placeholder, and base64-embeds the result into `src/host.html`.
- `src/host.html` is the shell: drop zone, JSONL parser (header + entries, leaf =
  last entry, adds ids to legacy v1 files), and an `<iframe srcdoc>` that renders the
  viewer with the data filled in. Drops over the iframe are forwarded to the host
  via `postMessage`.
- The theme is whatever `pi --export` uses by default at build time.

## Test

Headless Chrome smoke test (loads a file through the picker, checks that messages
render and the console has no errors):

```sh
npm install
npm test                                  # uses src/base-session.jsonl
node tests/smoke.js path/to/session.jsonl
CHROME=/path/to/chrome npm test           # non-default Chrome location
```

## Limitations

- Custom-tool TUI pre-rendering, system prompt and tool list are only in pi's HTML
  export, not in the `.jsonl`, so they are not shown here.
- Entries are loaded as-is; only v1 files get id/parentId backfilled (v2 → v3
  migrations are not applied).

## License

MIT. Bundles pi's export template and vendored libraries (marked, highlight.js),
which keep their own licenses.
