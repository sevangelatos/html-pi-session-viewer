#!/usr/bin/env python3
"""Build dist/session-viewer.html.

Runs `pi --export` on a tiny session to obtain pi's own viewer (CSS, JS,
marked, highlight.js, theme), swaps the embedded session data for a
placeholder, and wraps it in src/host.html (drag & drop shell).

Usage: ./build.py [path/to/existing-pi-export.html]
"""
import base64, os, re, subprocess, sys, tempfile
root = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) > 1:
    src = sys.argv[1]
else:
    src = os.path.join(tempfile.mkdtemp(), 'export.html')
    subprocess.run(['pi', '--export', os.path.join(root, 'src/base-session.jsonl'), src], check=True)

app = open(src, encoding='utf8').read()
m = re.search(r'(<script id="session-data" type="application/json">)(.*?)(</script>)', app, re.S)
if not m:
    sys.exit('session-data script not found; pi export format changed?')
app = app[:m.start(2)] + '__SESSION_DATA__' + app[m.end(2):]

# forward drops made inside the viewer iframe to the host page
fwd = '''<script>
addEventListener('dragover',e=>e.preventDefault());
addEventListener('drop',e=>{e.preventDefault();const f=e.dataTransfer.files[0];if(f)parent.postMessage({piFile:f},'*');});
</script></body>'''
i = app.rindex('</body>')
app = app[:i] + fwd + app[i + 7:]

b64 = base64.b64encode(app.encode()).decode()
host = open(os.path.join(root, 'src/host.html'), encoding='utf8').read().replace('__APP_B64__', b64)
out = os.path.join(root, 'dist/session-viewer.html')
open(out, 'w', encoding='utf8').write(host)
print('wrote', out, len(host) // 1024, 'KB')
