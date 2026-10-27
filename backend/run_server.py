import os
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def find_free_port(start_port: int, host: str = "127.0.0.1", max_tries: int = 25) -> int:
    for offset in range(max_tries):
        port = start_port + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free port found starting from {start_port}.")


if __name__ == "__main__":
    host = (os.getenv("HOST") or "127.0.0.1").strip() or "127.0.0.1"
    requested_port = int((os.getenv("PORT") or "8000").strip() or "8000")
    port = find_free_port(requested_port, host=host)

    if port != requested_port:
        print(f"Port {requested_port} is busy. Starting on {port} instead.")

    print(f"Starting VibeVault on http://{host}:{port}")
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", host, "--port", str(port)],
        cwd=str(ROOT),
        check=False,
    )
