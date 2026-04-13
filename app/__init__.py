"""SynapseOps application package.

This exposes an ASGI app object for platforms that auto-detect `app:app`.
"""

from app.api.server import create_app

app = create_app()

