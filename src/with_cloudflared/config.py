CLOUDFLARED_CONFIG = {
    ('Windows', 'AMD64'): {
        'command': 'cloudflared-windows-amd64.exe',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe'
    },
    ('Windows', 'x86'): {
        'command': 'cloudflared-windows-386.exe',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-386.exe'
    },
    ('Linux', 'x86_64'): {
        'command': 'cloudflared-linux-amd64',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64'
    },
    ('Linux', 'i386'): {
        'command': 'cloudflared-linux-386',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386'
    },
    ('Linux', 'arm'): {
        'command': 'cloudflared-linux-arm',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm'
    },
    ('Linux', 'arm64'): {
        'command': 'cloudflared-linux-arm64',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64'
    },
    ('Linux', 'aarch64'): {
        'command': 'cloudflared-linux-arm64',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64'
    },
    ('Darwin', 'x86_64'): {
        'command': 'cloudflared',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz'
    },
    ('Darwin', 'arm64'): {
        'command': 'cloudflared',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz'
    }
}