from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Configuração central da aplicação, lida de variáveis de ambiente."""

    model_path: Path
    host: str
    port: int
    debug: bool

    @classmethod
    def from_env(cls) -> "Settings":
        base_dir = Path(__file__).resolve().parents[3]
        default_model_path = base_dir / "models" / "modelo.pkl"
        return cls(
            model_path=Path(os.getenv("MODEL_PATH", str(default_model_path))),
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")),
            debug=os.getenv("DEBUG", "false").lower() == "true",
        )
