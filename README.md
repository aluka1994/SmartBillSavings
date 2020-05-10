# Cloud Computing Project 2 <br>
## Team Group 1 <br>
1.Rajashekar Reddy Aluka 1217211645 <br>
2.Pavan Kumar Bhalkey 1217204157 <br>
3.Pushparajsinh Zala 1217568222 <br>

## Development Setup Requirements

- Python 3.7 or later
- Windows, macOS, and Linux development environments are supported


## Development Setup Instructions

Assuming the development setup requirements above have been satisfied,
run the following in a terminal (git-bash is recommended on Windows) after cloning the repo
to set up your local development environment.

```bash 
# Install local dev requirements, ideally in an isolated Python 3.7 (or later) environment
pip install -r requirements-dev.txt
```


## Running the Development Server

If you're on Linux or macOS you can run the app via `gunicorn`, which offers a `--reload` option and
more closely emulates the App Engine production runtime, which uses gunicorn by default.

```bash
# Linux and macOS only, use --reload flag to automatically reload on code changes
gunicorn app:application --reload
```

```bash
# Cross-platform, works on Windows, macOS and Linux, albeit without a --reload option available
waitress-serve app:application
```

The app is viewable at http://localhost:8000 (for gunicorn) or at http://localhost:8080 (for Waitress).

The sample hello endpoint is at `http://$HOST:$PORT/api/v1/hello/world`

### Customizing the HTTP Port

The app runs on port 8000 (for gunicorn) and 8080 (for waitress) by default.  

To customize the port, pass the `--bind` option (for gunicorn) 
or the `--port` option (for Waitress) as in the following examples...

```bash
# Set gunicorn port to 9000
gunicorn --bind=:9000 app:application --reload

# Set Waitress port to 9000
waitress-serve --port=9000 app:application
```


## Running Tests

The tests are run via `pytest`, with the configuration file at `pytest.ini`.

```bash
# Run all tests
pytest

# Run only a particular test
pytest tests/test_api.py::test_hello

```


## Google Cloud Setup Instructions

The following steps only need to be performed once per local development environment...

1. Create an App Engine Project at https://console.cloud.google.com/appengine
2. Download and install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/)
3. If on Windows, run the "Google Cloud SDK Shell" application
4. Type `gcloud init` in a terminal or in the Cloud SDK Shell
5. Log in via `gcloud auth login` in a terminal or in Cloud SDK Shell as needed
6. Set the active project (created in step 1) via `gcloud config set project PROJECT_ID`
7. If on Windows or macOS, install the App Engine components via `gcloud components install app-engine-python`


## Deploying to Google App Engine

Ensure the project you want to deploy is selected via `gcloud config set project PROJECT_ID`, then
run the following command at the repo root (where the `app.yaml` config file is located) to deploy to App Engine...

```bash
# Deploy to App Engine
gcloud app deploy
```


## Google Cloud Function Deployment

```bash
gcloud functions deploy Translate --runtime=python37 --entry-point=subscribe --trigger-topic=ocr --set-env-vars GOOGLE_CLOUD_PROJECT=ccnew-275119,CLOUD_STORAGE_BUCKET=ccnew-275119.appspot.com,CLOUD_SQL_CONNECTION_NAME=ccnew-275119:us-east1:clouddb,DB_USER=raja,DB_PASS=cloudcc,DB_NAME=bdb
```
