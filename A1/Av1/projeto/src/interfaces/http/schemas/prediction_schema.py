from __future__ import annotations

from typing import Mapping

from src.domain.entities.air_quality_reading import FEATURE_ORDER, AirQualityReading


class ValidationError(ValueError):
    """Erro de validação de payload de entrada."""


class PredictionRequestSchema:
    """Valida e transforma o JSON de entrada em uma `AirQualityReading`.

    Responsabilidade única: garantir que o payload recebido pelo HTTP tem
    todos os campos esperados e com o tipo correto. Nenhuma regra de negócio
    mora aqui.
    """

    REQUIRED_FIELDS: tuple[str, ...] = FEATURE_ORDER

    def parse(self, payload: Mapping | None) -> AirQualityReading:
        if payload is None or not isinstance(payload, Mapping):
            raise ValidationError("Payload JSON ausente ou inválido.")

        missing = [f for f in self.REQUIRED_FIELDS if f not in payload]
        if missing:
            raise ValidationError(f"Campos ausentes: {', '.join(missing)}")

        parsed: dict[str, float] = {}
        for field in self.REQUIRED_FIELDS:
            value = payload[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValidationError(
                    f"Campo '{field}' deve ser numérico, recebido: {type(value).__name__}"
                )
            parsed[field] = float(value)

        return AirQualityReading.from_mapping(parsed)
