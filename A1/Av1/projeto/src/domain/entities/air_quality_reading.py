from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


FEATURE_ORDER: tuple[str, ...] = (
    "PT08.S1(CO)",
    "C6H6(GT)",
    "PT08.S2(NMHC)",
    "NOx(GT)",
    "PT08.S3(NOx)",
    "NO2(GT)",
    "PT08.S4(NO2)",
    "PT08.S5(O3)",
    "T",
    "RH",
    "AH",
)


@dataclass(frozen=True)
class AirQualityReading:
    """Leitura de sensores usada como entrada para regressão de CO(GT).

    A ordem das features é imutável e determinada em treino; violar a ordem
    quebra o contrato do modelo exportado (.pkl).
    """

    pt08_s1_co: float
    c6h6_gt: float
    pt08_s2_nmhc: float
    nox_gt: float
    pt08_s3_nox: float
    no2_gt: float
    pt08_s4_no2: float
    pt08_s5_o3: float
    temperature: float
    relative_humidity: float
    absolute_humidity: float

    @classmethod
    def from_mapping(cls, data: Mapping[str, float]) -> "AirQualityReading":
        return cls(
            pt08_s1_co=float(data["PT08.S1(CO)"]),
            c6h6_gt=float(data["C6H6(GT)"]),
            pt08_s2_nmhc=float(data["PT08.S2(NMHC)"]),
            nox_gt=float(data["NOx(GT)"]),
            pt08_s3_nox=float(data["PT08.S3(NOx)"]),
            no2_gt=float(data["NO2(GT)"]),
            pt08_s4_no2=float(data["PT08.S4(NO2)"]),
            pt08_s5_o3=float(data["PT08.S5(O3)"]),
            temperature=float(data["T"]),
            relative_humidity=float(data["RH"]),
            absolute_humidity=float(data["AH"]),
        )

    def as_feature_vector(self) -> list[float]:
        return [
            self.pt08_s1_co,
            self.c6h6_gt,
            self.pt08_s2_nmhc,
            self.nox_gt,
            self.pt08_s3_nox,
            self.no2_gt,
            self.pt08_s4_no2,
            self.pt08_s5_o3,
            self.temperature,
            self.relative_humidity,
            self.absolute_humidity,
        ]
