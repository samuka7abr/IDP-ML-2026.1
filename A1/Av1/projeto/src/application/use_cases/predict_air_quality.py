from __future__ import annotations

from src.application.dtos.prediction_dto import PredictionInputDTO, PredictionOutputDTO
from src.application.interfaces.model_predictor import ModelPredictor
from src.domain.value_objects.air_quality_category import AirQualityClassificationRule


class PredictAirQualityUseCase:
    """Orquestra a predição de CO(GT) e a classificação qualitativa do ar.

    Recebe colaboradores via injeção de dependência, preservando o Dependency
    Inversion Principle — o caso de uso não conhece scikit-learn nem Flask.
    """

    def __init__(
        self,
        predictor: ModelPredictor,
        classification_rule: AirQualityClassificationRule,
    ) -> None:
        self._predictor = predictor
        self._rule = classification_rule

    def execute(self, input_dto: PredictionInputDTO) -> PredictionOutputDTO:
        features = input_dto.reading.as_feature_vector()
        co_value = self._predictor.predict(features)
        category = self._rule.classify(co_value)
        return PredictionOutputDTO(co_gt_predicted=co_value, air_quality=category)
