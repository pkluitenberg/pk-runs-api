# PK Runs API

This is a simple REST API created using Python & FastApi. This api surfaces my personal running data from the past few years.

The api is currently hosted at https://pk-runs-api.up.railway.app/ 

Documentation and interactive access can be found at the `/docs` endpoint.

The application sits inside the `src` folder.

Unit tests can be found in `src/tests`.

Environment variables can be found in the `.env` folder.

## Install

    # create virtual env
    python3 -m venv env

    #activate virtual env
    source env/bin/activate

    # install dependencies
    pip install -r requirements.txt

## Run the app

    uvicorn src.main:app --reload --port 8000

## Run the tests

    pytest

## Populate environment variables

    # .env variables
    STRAVA_CLIENT_ID=
    STRAVA_CLIENT_SECRET=
    STRAVA_API_REFRESH_TOKEN=
    STRAVA_ATHLETE_ID=
    MONGOHOST=
    MONGOPASSWORD=
    MONGOPORT=
    MONGOUSER=
    STRAVA_SUBSCRIPTION_VERIFICATION_TOKEN=