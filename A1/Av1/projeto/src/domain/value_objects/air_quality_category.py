from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AirQualityCategory(str, Enum):
    """Classificação qualitativa do ar a partir do valor de CO(GT) (mg/m³)."""

    BOM = "bom"
    MEDIO = "medio"
    RUIM = "ruim"


@dataclass(frozen=True)
class AirQualityClassificationRule:
    """Regras de faixa definidas na AV1.

    - bom:   CO(GT) <= 4
    - medio: 4 < CO(GT) <= 9
    - ruim:  CO(GT) > 9
    """

    bom_upper: float = 4.0
    medio_upper: float = 9.0

    def classify(self, co_value: float) -> AirQualityCategory:
        if co_value <= self.bom_upper:
            return AirQualityCategory.BOM
        if co_value <= self.medio_upper:
            return AirQualityCategory.MEDIO
        return AirQualityCategory.RUIM
