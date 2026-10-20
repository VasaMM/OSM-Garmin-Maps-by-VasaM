"""Exercise resumed byte ranges and changed remote revisions without external traffic."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from docker import fetch_inputs as fetch


class DownloadTest(unittest.TestCase):
    def test_resume_and_revision_change(self):
        data = b"a map input" * 100
        class Handler(BaseHTTPRequestHandler):
            def do_HEAD(self):
                self.send_response(200)
                self.send_header('Content-Length', str(len(data)))
                self.send_header('ETag', 'current')
                self.end_headers()
            def do_GET(self):
                start, end = map(int, self.headers['Range'][6:].split('-'))
                self.send_response(206)
                self.send_header('Content-Range', f'bytes {start}-{end}/{len(data)}')
                self.send_header('Content-Length', str(end-start+1))
                self.send_header('ETag', 'current')
                self.end_headers()
                self.wfile.write(data[start:end+1])
            def log_message(self, *args): pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as tmp, patch.object(fetch, 'CHUNK', 64):
                url = f'http://127.0.0.1:{server.server_port}/map'
                path = Path(tmp) / 'input.pbf'
                plan, jobs = fetch.prepare(url, path)
                parts = plan[1]
                (parts/'0').write_bytes(data[:17])  # interrupted first range
                fetch.fetch_all([(url, path)])
                self.assertEqual(path.read_bytes(), data)
                self.assertFalse(parts.exists())
                path.unlink()
                plan, jobs = fetch.prepare(url, path)
                (parts/'0').write_bytes(b'x'*64)
                (parts/'source.json').write_text(json.dumps({'etag': 'old'}))
                fetch.fetch_all([(url, path)])
                self.assertEqual(path.read_bytes(), data)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == '__main__': unittest.main()
