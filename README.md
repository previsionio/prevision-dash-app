# prevision-dash-app

## Project architecture


A `run.py` file at root of your folder

## Setup

- create an env ( better )
- activate it
- install requirements
- fill the .env fie with your model url, id and secret
- launch the app with gunicorn


```
python -m venv env
source env/bin/activate
pip install -r requirements.txt 
gunicorn --bind 0.0.0.0:8080  --threads 10 -w 2 --timeout 120 --limit-request-line 0 --access-logfile - run:app
```


### Warning

Your app with be launched with Gunicorn and the following option :

`gunicorn --bind 0.0.0.0:8080  --threads 10 -w 2 --timeout 120 --limit-request-line 0 --access-logfile - run:app`

Check that you "main" file is named `run.py` and that the dash app server is bind to the app variable :

```
dashboard = dash.Dash(__name__) 
app = dashboard.server
```