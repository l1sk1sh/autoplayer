#!/usr/bin/env bash
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
python -m virtualenv .venv --python=python3.7 
source .venv/bin/activate 
python -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
python .venv/bin/pywin32_postinstall.py -install