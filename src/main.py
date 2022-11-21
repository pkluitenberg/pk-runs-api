import os

from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer

from src.gcp.storage import read_json_from_google_cloud_storage
from src.models.event import Event
from src.strava.strava_event import StravaEvent

load_dotenv()


GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')

app = FastAPI(title='PK Runs API')

api_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    'http://pk-runs.herokuapp.com',
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api_router.get('/')
async def root():
    return "wyd?"


@api_router.get('/all_activities')
def all_activities():
    content = read_json_from_google_cloud_storage(
        bucket=GCS_BUCKET_NAME, filename='allActivities.json')
    return JSONResponse(content=content)


@api_router.get('/all_stats')
def all_activities():
    content = read_json_from_google_cloud_storage(
        bucket=GCS_BUCKET_NAME, filename='allStats.json')
    return JSONResponse(content=content)


@api_router.get('/events')
def event_subscription_validation(token: str = Query(default=None, alias="hub.verify_token"),
                                  challenge: str = Query(
                                      default=None, alias="hub.challenge"),
                                  mode: str = Query(default=None, alias="hub.mode")):
    verify_token = 'distort-baffling-immortal-unlatch-showy'

    if mode and token:
        if mode == 'subscribe' and token == verify_token:
            print('WEBHOOK_VERIFIED')
            return JSONResponse(content={"hub.challenge": challenge}, status_code=200)
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@api_router.post('/events')
async def event(event: Event, background_tasks: BackgroundTasks):
    # need this to return 200 asyncronously
    # need this to validate that it's a legit event before it get's started
    print(event)
    if event.object_type == 'activity':
        activity_id = event.object_id
        if event.aspect_type == 'create':
            background_tasks.add_task(StravaEvent.create, activity_id)
        if event.aspect_type == 'delete':
            background_tasks.add_task(StravaEvent.delete, activity_id)
    else:
        pass
    return Response(status_code=status.HTTP_200_OK)


app.include_router(api_router)
