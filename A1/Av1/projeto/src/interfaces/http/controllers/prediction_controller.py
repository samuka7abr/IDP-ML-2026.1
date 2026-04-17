from __future__ import annotations

from flask import Blueprint, jsonify, request

from src.application.dtos.prediction_dto import PredictionInputDTO
from src.application.use_cases.predict_air_quality import PredictAirQualityUseCase
from src.interfaces.http.schemas.prediction_schema import PredictionRequestSchema


EXAMPLE_PAYLOAD = {
    "PT08.S1(CO)": 1360.0,
    "C6H6(GT)": 11.9,
    "PT08.S2(NMHC)": 1046.0,
    "NOx(GT)": 166.0,
    "PT08.S3(NOx)": 1056.0,
    "NO2(GT)": 113.0,
    "PT08.S4(NO2)": 1692.0,
    "PT08.S5(O3)": 1268.0,
    "T": 13.6,
    "RH": 48.9,
    "AH": 0.7578,
}


def build_prediction_blueprint(
    use_case: PredictAirQualityUseCase,
    schema: PredictionRequestSchema,
) -> Blueprint:
    """Factory do blueprint com dependências injetadas — sem estado global."""

    blueprint = Blueprint("prediction", __name__)

    @blueprint.route("/health", methods=["GET"])
    def health():
        """Healthcheck simples.
        ---
        tags:
          - meta
        responses:
          200:
            description: API saudável.
        """
        return jsonify({"status": "ok"})

    @blueprint.route("/example", methods=["GET"])
    def example():
        """Predição de exemplo com payload fixo.
        ---
        tags:
          - predict
        responses:
          200:
            description: Resultado da predição de exemplo.
        """
        reading = schema.parse(EXAMPLE_PAYLOAD)
        output = use_case.execute(PredictionInputDTO(reading=reading))
        return jsonify({"input": EXAMPLE_PAYLOAD, **output.to_dict()})

    @blueprint.route("/predict", methods=["POST"])
    def predict():
        """Prediz CO(GT) e classifica a qualidade do ar.
        ---
        tags:
          - predict
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - PT08.S1(CO)
                - C6H6(GT)
                - PT08.S2(NMHC)
                - NOx(GT)
                - PT08.S3(NOx)
                - NO2(GT)
                - PT08.S4(NO2)
                - PT08.S5(O3)
                - T
                - RH
                - AH
              properties:
                PT08.S1(CO): {type: number, example: 1360.0}
                C6H6(GT): {type: number, example: 11.9}
                PT08.S2(NMHC): {type: number, example: 1046.0}
                NOx(GT): {type: number, example: 166.0}
                PT08.S3(NOx): {type: number, example: 1056.0}
                NO2(GT): {type: number, example: 113.0}
                PT08.S4(NO2): {type: number, example: 1692.0}
                PT08.S5(O3): {type: number, example: 1268.0}
                T: {type: number, example: 13.6}
                RH: {type: number, example: 48.9}
                AH: {type: number, example: 0.7578}
        responses:
          200:
            description: Predição e classificação qualitativa.
            schema:
              type: object
              properties:
                co_gt_predicted: {type: number}
                air_quality: {type: string, enum: [bom, medio, ruim]}
          400:
            description: Payload inválido.
        """
        reading = schema.parse(request.get_json(silent=True))
        output = use_case.execute(PredictionInputDTO(reading=reading))
        return jsonify(output.to_dict())

    return blueprint
