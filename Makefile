lint:
	pylint twitchvod/ tests/

test:
	pytest

coverage:
	pytest --cov-report term-missing --cov=twitchvod/ tests/
