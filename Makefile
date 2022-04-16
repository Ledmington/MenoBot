RUN=poetry run

.PHONY: cov

update:
	poetry update
	poetry lock

install:
	poetry install

run:
	${RUN} python3 menobot/menobot/main.py

cov:
	${RUN} pytest --cov-config=.cov_config --cov-report html:cov_report --cov=./menobot ./menobot/tests

format:
	${RUN} black .

todo:
	find . | grep .py$$ | grep -rnw . -e TODO

clean:
	rm -rf cov_report dist .idea .ipynb_checkpoints
	rm -f .coverage*
	find ./ | grep __pycache__$ | xargs rm -rf
	find ./ | grep .pytest_cache$ | xargs rm -rf
