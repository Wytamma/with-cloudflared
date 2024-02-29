import tarfile
import tempfile
import shutil
import platform
import urllib.request
from pathlib import Path
from .config import CLOUDFLARED_CONFIG

def get_command(system, machine):
    try:
        return CLOUDFLARED_CONFIG[(system, machine)]['command']
    except KeyError:
        raise Exception(f"{machine} is not supported on {system}")

def get_url(system, machine):
    try:
        return CLOUDFLARED_CONFIG[(system, machine)]['url']
    except KeyError:
        raise Exception(f"{machine} is not supported on {system}")

# Needed for the darwin package
def extract_tarball(tar_path, filename):
    tar = tarfile.open(tar_path+'/'+filename, 'r')
    for item in tar:
        tar.extract(item, tar_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            tar.extract(item.name, "./" + item.name[:item.name.rfind('/')])


def download_cloudflared(cloudflared_path, command, force=False):
    if Path(cloudflared_path, command).exists() and not force:
        return
    system, machine = platform.system(), platform.machine()
    url = get_url(system, machine)
    download_file(url)

def download_file(url):
    local_filename = url.split('/')[-1]
    # download files using urllib
    download_path = str(Path(tempfile.gettempdir(), local_filename))
    with urllib.request.urlopen(url) as response:
        with open(download_path, 'wb') as f:
            shutil.copyfileobj(response, f)
    return download_path

