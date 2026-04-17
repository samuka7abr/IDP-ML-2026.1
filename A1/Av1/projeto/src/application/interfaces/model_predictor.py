from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence


class ModelPredictor(ABC):
    """Port (Dependency Inversion) da camada de aplicação.

    A aplicação depende desta abstração, não de scikit-learn diretamente.
    Qualquer implementação (sklearn, ONNX, stub de teste) deve respeitar esse
    contrato.
    """

    @abstractmethod
    def predict(self, features: Sequence[float]) -> float:
        """Recebe o vetor de features na ordem canônica e devolve o valor previsto."""
