from fastapi import APIRouter, FastAPI, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer
from src.gcp.storage import read_json_from_google_cloud_storage
from src.models.event import Event

GCS_BUCKET_NAME = 'pk-runs-data'

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
def event(event: Event):
    print(event)
    return Response(status_code=status.HTTP_200_OK)


app.include_router(api_router)
