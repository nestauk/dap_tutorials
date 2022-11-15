SHELL := /bin/bash

export REPO_NAME=abm_demo

.PHONY: install
## Install a project: create conda env; install local package; setup git hooks
install:
	@echo -n "Creating environment ${REPO_NAME} and installing all dependencies"
	@(conda env create -q -n ${REPO_NAME} -f environment.yaml\
		&& eval "$$(conda shell.bash activate "${REPO_NAME}")"\
		&& pip install -r requirements.txt)
	@touch $@
	@echo " DONE"

.PHONY: conda-update
## Update the conda-environment based on changes to `environment.yaml`
conda-update:
	conda env update -n ${REPO_NAME} -f environment.yaml
	$(MAKE) -s pip-install
	direnv reload

.PHONY: pip-install
## Install our package and requirements in editable mode (including development dependencies)
pip-install:
	@pip install -e ".[dev]"