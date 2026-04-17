COMPOSE := docker compose -f docker/docker-compose.yml
API_URL ?= http://localhost:5000

.PHONY: up down build clean test logs

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build --no-cache

logs:
	$(COMPOSE) logs -f

test:
	@command -v jq >/dev/null || { echo "jq não encontrado — instale com: sudo dnf install jq"; exit 1; }
	@echo "→ GET /health"
	@curl -fsS $(API_URL)/health | jq .
	@echo "→ GET /example"
	@curl -fsS $(API_URL)/example | jq '{air_quality, co_gt_predicted}'
	@echo "→ POST /predict  (bom.json)"
	@curl -fsS -X POST $(API_URL)/predict -H 'Content-Type: application/json' -d @examples/bom.json | jq .
	@echo "→ POST /predict  (medio.json)"
	@curl -fsS -X POST $(API_URL)/predict -H 'Content-Type: application/json' -d @examples/medio.json | jq .
	@echo "→ POST /predict  (ruim.json)"
	@curl -fsS -X POST $(API_URL)/predict -H 'Content-Type: application/json' -d @examples/ruim.json | jq .
	@echo "→ POST /predict  (payload inválido — espera HTTP 400)"
	@resp=$$(curl -sS -o /dev/stdout -w '\n%{http_code}' -X POST $(API_URL)/predict -H 'Content-Type: application/json' -d '{}'); \
	 body=$$(echo "$$resp" | head -n -1); \
	 code=$$(echo "$$resp" | tail -n 1); \
	 echo "$$body" | jq .; \
	 echo "HTTP $$code"

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
