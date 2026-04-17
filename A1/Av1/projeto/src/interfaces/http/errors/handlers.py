from __future__ import annotations

import logging

from flask import Flask, jsonify

from src.interfaces.http.schemas.prediction_schema import ValidationError

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """Registra tratadores globais para converter exceções em respostas JSON.

    Mantém os controllers finos: eles só precisam levantar a exceção correta.
    """

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError):
        return jsonify({"error": "validation_error", "message": str(exc)}), 400

    @app.errorhandler(ValueError)
    def handle_value_error(exc: ValueError):
        return jsonify({"error": "invalid_input", "message": str(exc)}), 400

    @app.errorhandler(404)
    def handle_not_found(_exc):
        return jsonify({"error": "not_found", "message": "Rota inexistente."}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(_exc):
        return (
            jsonify({"error": "method_not_allowed", "message": "Método HTTP não permitido."}),
            405,
        )

    @app.errorhandler(Exception)
    def handle_unexpected(exc: Exception):
        logger.exception("Erro inesperado: %s", exc)
        return jsonify({"error": "internal_error", "message": "Erro interno do servidor."}), 500
