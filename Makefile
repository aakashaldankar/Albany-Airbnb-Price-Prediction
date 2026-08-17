.PHONY: help dev down train lint test deploy destroy

help:
	@echo "Available targets:"
	@echo "  make dev      - start the full local stack (docker compose up --build)"
	@echo "  make down     - stop the local stack"
	@echo "  make train    - run the DVC training pipeline once"
	@echo "  make lint     - run ruff over app/ and src/"
	@echo "  make test     - run lint + unit + integration tests, same as CI"
	@echo "  make deploy   - how to ship a change (CI/CD is push-to-main, not local)"
	@echo "  make destroy  - terraform destroy the AWS infrastructure"

dev:
	docker compose up --build

down:
	docker compose down

train:
	docker compose --profile train run --rm dvc-service

lint:
	ruff check app src

test: lint
	pytest tests/unit --cov=app --cov=src --cov-report=term-missing --cov-fail-under=65
	pytest tests/integration -m 'not slow' --cov=app --cov=src --cov-append --cov-report=term-missing --cov-fail-under=65

deploy:
	@echo "Deployment is CI/CD-driven, not a local command."
	@echo "Push to main and .github/workflows/deploy.yml builds, pushes, and rolls"
	@echo "out every service, with an automatic rollback if the smoke test fails:"
	@echo ""
	@echo "  git push origin main"

destroy:
	cd terraform && terraform destroy
