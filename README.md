# Flask Backend
### Get Started
- Set the environment variables for your local machine in ```config/config.py```
- Set the virtual environment(venv) by using command ```python -m venv <name_of venv>```
- Activate the virtual environment ```.\<name_of venv>\Scripts\activate```
- Set the environment variables:
```
$env:FLASK_APP='base.py'
$env:FLASK_ENV="development"
$env:PYTHONDONTWRITEBYTECODE=1
```
- Run the flask app ```flask run --debug```