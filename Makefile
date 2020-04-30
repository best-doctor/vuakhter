test:
	python -m pytest --cov=vuakhter --cov-report=xml

types:
	mypy vuakhter

style:
	flake8 vuakhter
	mdl README.md

check:
	make style
	make types
	make test
