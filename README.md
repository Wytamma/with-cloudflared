# with-cloudflared

With-cloudflared provides a context manager to start and stop cloudflared. Cloudflare Tunnel provides you with a secure way to connect your resources to Cloudflare without a publicly routable IP address. This is useful for development and testing, as well as for production use cases. See the [Cloudflare Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) for more information.

## Installation

```bash
pip install with-cloudflared
```

## Usage

```python
import uvicorn
from fastapi import FastAPI
from with_cloudflared import cloudflared

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    port = 8000
    with cloudflared(port=port) as cloudflared_address:
        print(f" * Running on {cloudflared_address}")
        uvicorn.run(app, port=port)
```

This will start cloudflared and then start the FastAPI server. The app will be publicly available at the cloudflared address e.g. something like `https://rp-son-configured-army.trycloudflare.com`.

The first time you run this it will take a few seconds to download and start cloudflared. Subsequent runs will be much faster.