from __future__ import annotations

from pathlib import Path
from typing import Sequence

import joblib
import pandas as pd

from src.application.interfaces.model_predictor import ModelPredictor
from src.domain.entities.air_quality_reading import FEATURE_ORDER


class SklearnModelPredictor(ModelPredictor):
    """Adapter concreto que carrega um artefato sklearn `.pkl`.

    O artefato é um dicionário contendo ao menos as chaves `model` (pipeline
    sklearn) e `features` (ordem canônica das features usadas em treino).
    A aplicação só conhece a port `ModelPredictor`; este módulo é o único
    ponto do código que importa sklearn/joblib.
    """

    def __init__(self, model_path: Path) -> None:
        if not model_path.exists():
            raise FileNotFoundError(f"Modelo não encontrado em {model_path}")

        artifact = joblib.load(model_path)
        self._model = artifact["model"]

        artifact_features = tuple(artifact.get("features", FEATURE_ORDER))
        if artifact_features != FEATURE_ORDER:
            raise ValueError(
                "Ordem de features do artefato diverge do domínio. "
                f"Esperado {FEATURE_ORDER}, obtido {artifact_features}."
            )

    def predict(self, features: Sequence[float]) -> float:
        if len(features) != len(FEATURE_ORDER):
            raise ValueError(
                f"Vetor de features inválido: esperado {len(FEATURE_ORDER)} valores, "
                f"recebido {len(features)}."
            )
        frame = pd.DataFrame([list(features)], columns=list(FEATURE_ORDER))
        prediction = self._model.predict(frame)
        return float(prediction[0])
