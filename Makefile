# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* tiniworld_core/*.py

black:
	@black scripts/* tiniworld_core/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr tiniworld_core-*.dist-info
	@rm -fr tiniworld_core.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)


# --------------------------------------
#      Model Training and predictions
# --------------------------------------

PYPI_USERNAME=<AUTHOR>
# Train a forecast model for entire dataset as a whole to see trend/seasonality of whole company
run_train_all:
        #python -c 'from taxifare.interface.main import train; train()'
				python -c 'from tiniworld_core.interface.main import run_train_consolidated_stores ;run_train_consolidated_stores()';

PYPI_USERNAME=<AUTHOR>
# Train a forecast model for every single location
run_train_single:
				python -c 'from tiniworld_core.interface.main import train_single_store; train_single_store()';
