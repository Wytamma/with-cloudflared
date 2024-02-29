import tarfile
import tempfile
import shutil
import platform
import urllib.request
from pathlib import Path
from .config import CLOUDFLARED_CONFIG

def get_command(system, machine):
    """
    Retrieves the command for a given system and machine from the CLOUDFLARED_CONFIG.

    Args:
      system (str): The system for which the command is needed.
      machine (str): The machine for which the command is needed.

    Returns:
      str: The command for the given system and machine.

    Raises:
      Exception: If the machine is not supported on the system.

    Examples:
      >>> get_command('Linux', 'x86_64')
      'cloudflared'
    """
    try:
        return CLOUDFLARED_CONFIG[(system, machine)]['command']
    except KeyError:
        raise Exception(f"{machine} is not supported on {system}")

def get_url(system, machine):
    """
    Retrieves the URL for a given system and machine from the CLOUDFLARED_CONFIG.

    Args:
      system (str): The system for which the URL is needed.
      machine (str): The machine for which the URL is needed.

    Returns:
      str: The URL for the given system and machine.

    Raises:
      Exception: If the machine is not supported on the system.

    Examples:
      >>> get_url('Linux', 'x86_64')
      'https://bin.equinox.io/c/VdrWdbjqyF/cloudflared-stable-linux-amd64.tgz'
    """
    try:
        return CLOUDFLARED_CONFIG[(system, machine)]['url']
    except KeyError:
        raise Exception(f"{machine} is not supported on {system}")

# Needed for the darwin package
def extract_tarball(tar_path, filename):
    """
    Extracts a tarball file at a given path.

    Args:
      tar_path (str): The path where the tarball file is located.
      filename (str): The name of the tarball file.

    Side Effects:
      Extracts the tarball file at the given path.

    Examples:
      >>> extract_tarball('/path/to/tarball', 'file.tar.gz')
    """
    tar = tarfile.open(tar_path+'/'+filename, 'r')
    for item in tar:
        tar.extract(item, tar_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            tar.extract(item.name, "./" + item.name[:item.name.rfind('/')])


def download_cloudflared(cloudflared_path, command, force=False):
    """
    Downloads the cloudflared binary if it does not exist or if force is True.

    Args:
      cloudflared_path (str): The path where the cloudflared binary should be saved.
      command (str): The command to run.
      force (bool, optional): Whether to force the download even if the file exists. Defaults to False.

    Side Effects:
      Downloads the cloudflared binary.

    Examples:
      >>> download_cloudflared('/path/to/cloudflared', 'cloudflared', force=True)
    """
    if Path(cloudflared_path, command).exists() and not force:
        return
    system, machine = platform.system(), platform.machine()
    url = get_url(system, machine)
    download_file(url)

def download_file(url):
    """
    Downloads a file from a given URL.

    Args:
      url (str): The URL of the file to download.

    Returns:
      str: The path where the file was downloaded.

    Side Effects:
      Downloads a file from a given URL.

    Examples:
      >>> download_file('https://example.com/file.txt')
      '/tmp/file.txt'
    """
    local_filename = url.split('/')[-1]
    # download files using urllib
    download_path = str(Path(tempfile.gettempdir(), local_filename))
    with urllib.request.urlopen(url) as response:
        with open(download_path, 'wb') as f:
            shutil.copyfileobj(response, f)
    return download_path

