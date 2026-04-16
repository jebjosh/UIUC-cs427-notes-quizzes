from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

if __name__ == "__main__":
    port = 5799
    server = ThreadingHTTPServer(("", port), NoCacheHandler)
    print(f"Serving on http://localhost:{port} with cache disabled")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
