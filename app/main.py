"""SynapseOps application entrypoint.

This file is intentionally lightweight so it can evolve into API, worker,
or CLI startup logic as the project architecture is finalized.
"""

from __future__ import annotations

import logging


def configure_logging(level: int = logging.INFO) -> None:
	"""Configure basic logging for local development."""
	logging.basicConfig(
		level=level,
		format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
	)


def main() -> None:
	"""Application startup hook."""
	configure_logging()
	logging.getLogger(__name__).info("SynapseOps starter initialized.")


if __name__ == "__main__":
	main()
