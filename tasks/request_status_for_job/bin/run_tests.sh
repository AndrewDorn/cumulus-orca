cd ".."
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
# Currenty just running unit tests until we fix/support large tests
coverage run --source test/unit_tests/ -m pytest test/unit_tests/
result=$?
if [[ $result -eq 1 ]]; then
  return 1
fi
coverage report
deactivate
return 0
