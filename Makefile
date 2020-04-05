.PHONY: clean
.PHONY: install

clean:
	find . -type d -name __pycache__ -exec rm -r {} +

install: clean
	python setup.py install
