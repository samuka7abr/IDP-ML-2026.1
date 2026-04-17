from __future__ import annotations

import logging

from flasgger import Swagger
from flask import Flask, redirect

from src.application.use_cases.predict_air_quality import PredictAirQualityUseCase
from src.domain.value_objects.air_quality_category import AirQualityClassificationRule
from src.infrastructure.config.settings import Settings
from src.infrastructure.ml.sklearn_model_predictor import SklearnModelPredictor
from src.interfaces.http.controllers.prediction_controller import (
    build_prediction_blueprint,
)
from src.interfaces.http.errors.handlers import register_error_handlers
from src.interfaces.http.schemas.prediction_schema import PredictionRequestSchema


SWAGGER_TEMPLATE = {
    "info": {
        "title": "Air Quality API — AV1 IDP ML 2026.1",
        "description": (
            "API de serving para o modelo de regressão de CO(GT). "
            "Recebe leituras de sensores e devolve o valor previsto de CO(GT) "
            "junto com a classificação qualitativa do ar (bom / medio / ruim)."
        ),
        "version": "1.0.0",
    }
}


def create_app(settings: Settings | None = None) -> Flask:
    """Application factory — compõe a aplicação com injeção de dependências.

    Aqui é onde as camadas se encaixam: o HTTP (Flask) conhece o caso de uso
    (application), que conhece a port `ModelPredictor`. A implementação
    concreta (sklearn) é injetada neste ponto e em nenhum outro.
    """

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    settings = settings or Settings.from_env()

    predictor = SklearnModelPredictor(model_path=settings.model_path)
    classification_rule = AirQualityClassificationRule()
    use_case = PredictAirQualityUseCase(
        predictor=predictor,
        classification_rule=classification_rule,
    )
    schema = PredictionRequestSchema()

    app = Flask(__name__)
    Swagger(app, template=SWAGGER_TEMPLATE)

    app.register_blueprint(build_prediction_blueprint(use_case=use_case, schema=schema))
    register_error_handlers(app)

    @app.route("/", methods=["GET"])
    def root():
        return redirect("/apidocs")

    return app
