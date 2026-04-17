from __future__ import annotations

from dataclasses import dataclass

from src.domain.entities.air_quality_reading import AirQualityReading
from src.domain.value_objects.air_quality_category import AirQualityCategory


@dataclass(frozen=True)
class PredictionInputDTO:
    reading: AirQualityReading


@dataclass(frozen=True)
class PredictionOutputDTO:
    co_gt_predicted: float
    air_quality: AirQualityCategory

    def to_dict(self) -> dict:
        return {
            "co_gt_predicted": round(self.co_gt_predicted, 4),
            "air_quality": self.air_quality.value,
        }
