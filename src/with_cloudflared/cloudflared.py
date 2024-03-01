from contextlib import contextmanager
import subprocess
import tempfile
import os
import platform
import time
import re
from random import randint
import urllib.request
from pathlib import Path
from .utils import get_command, extract_tarball, download_cloudflared

@contextmanager
def cloudflared(port=8000, metrics_port=None, tunnel_id=None, config_path=None, force=False, max_retries=10):
    """
    A context manager for running a Cloudflare tunnel. It downloads the appropriate Cloudflare binary, starts the tunnel, and yields the tunnel URL. After the context is exited, it terminates the tunnel.

    Args:
      port (int, optional): The local port to tunnel. Defaults to 8000.
      metrics_port (int, optional): The port to serve metrics on. If not provided, a random port between 8100 and 9000 is chosen.
      tunnel_id (str, optional): The ID of the tunnel to run. If not provided, a tunnel to the local port is created.
      config_path (str, optional): The path to a Cloudflare configuration file. If provided, the 'run' command is used with this configuration.
      force (bool, optional): If True, forces the download of the Cloudflare binary even if it already exists. Defaults to False.
      max_retries (int, optional): The maximum number of times to retry connecting to the Cloudflare Edge. Defaults to 10.

    Yields:
      str: The URL of the Cloudflare tunnel.

    Raises:
      Exception: If it can't connect to the Cloudflare Edge after max_retries attempts.

    Side Effects:
      Downloads the Cloudflare binary, starts a subprocess running the Cloudflare tunnel, and modifies the permissions of the Cloudflare binary.

    Examples:
      >>> with cloudflared(port=8080) as url:
      ...     print(f"Cloudflare tunnel running at {url}")
      Cloudflare tunnel running at https://randomsubdomain.trycloudflare.com
    """
    if metrics_port is None:
        metrics_port = randint(8100, 9000)
    system, machine = platform.system(), platform.machine()
    command = get_command(system, machine)
    cloudflared_path = str(Path(tempfile.gettempdir()))
    if system == "Darwin":
        download_cloudflared(cloudflared_path, "cloudflared-darwin-amd64.tgz", force)
        extract_tarball(cloudflared_path, "cloudflared-darwin-amd64.tgz")
    else:
        download_cloudflared(cloudflared_path, command, force)

    executable = str(Path(cloudflared_path, command))
    os.chmod(executable, 0o777)

    cloudflared_command = [executable, 'tunnel', '--metrics', f'127.0.0.1:{metrics_port}']
    if config_path:
        cloudflared_command += ['--config', config_path, 'run']
    elif tunnel_id:
        cloudflared_command += ['--url', f'http://127.0.0.1:{port}', 'run', tunnel_id]
    else:
        cloudflared_command += ['--url', f'http://127.0.0.1:{port}']
    try:
        if system == "Darwin" and machine == "arm64":
            cloudflared_process = subprocess.Popen(['arch', '-x86_64'] + cloudflared_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            cloudflared_process = subprocess.Popen(cloudflared_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        localhost_url = f"http://127.0.0.1:{metrics_port}/metrics"

        for _ in range(max_retries):
            try:
                with urllib.request.urlopen(localhost_url) as response:
                    metrics = response.read().decode('utf-8')
                if tunnel_id or config_path:
                    # If tunnel_id or config_path is provided, we check for cloudflared_tunnel_ha_connections, as no tunnel URL is available in the metrics
                    if re.search(r"cloudflared_tunnel_ha_connections\s\d", metrics):
                        # No tunnel URL is available in the metrics, so we return a generic text
                        tunnel_url = "preconfigured tunnel URL"
                        break
                else:
                    # If neither tunnel_id nor config_path is provided, we check for the tunnel URL in the metrics
                    tunnel_url = (re.search(r"(?P<url>https?:\/\/[^\s]+.trycloudflare.com)", metrics).group("url"))
                    break
            except Exception:
                time.sleep(3)
        else:
            raise Exception("Can't connect to Cloudflare Edge!")
        yield tunnel_url
    finally:
        # Cleanup phase
        cloudflared_process.terminate()
        cloudflared_process.wait()


