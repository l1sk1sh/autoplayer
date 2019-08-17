@ECHO ON
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
python -m venv .venv
call .\.venv\Scripts\activate.bat
python -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
EXIT 0
