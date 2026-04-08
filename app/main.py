"""SynapseOps application entrypoint."""

from __future__ import annotations

import logging

from app.api.server import create_app
from app.config import Settings
from app.utils.logging import configure_logging

def main() -> None:
	"""Start the local API service."""
	settings = Settings.from_env()
	configure_logging(settings.log_level)

	logger = logging.getLogger(__name__)
	logger.info(
		"Starting %s in %s mode on %s:%s",
		settings.app_name,
		settings.app_env,
		settings.host,
		settings.port,
	)

	try:
		import uvicorn
	except ModuleNotFoundError as exc:  # pragma: no cover - runtime path
		raise RuntimeError("uvicorn is not installed. Run 'pip install -r requirements.txt'.") from exc

	uvicorn.run(create_app(settings), host=settings.host, port=settings.port)


if __name__ == "__main__":
	main()

