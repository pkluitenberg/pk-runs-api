from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from src.gcp.storage import read_json_from_google_cloud_storage

GCS_BUCKET_NAME = 'pk-runs-data'

app = FastAPI(title='PK Runs API')

api_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://pk-runs.herokuapp.com"
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


app.include_router(api_router)
