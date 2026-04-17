"""Entry point da camada de serving.

Mantido intencionalmente mínimo — toda a composição mora em
`src/interfaces/http/app_factory.py` (Clean Architecture).
"""
from __future__ import annotations

from src.infrastructure.config.settings import Settings
from src.interfaces.http.app_factory import create_app


settings = Settings.from_env()
app = create_app(settings)


if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug)
