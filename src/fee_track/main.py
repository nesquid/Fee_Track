import uvicorn
from fastapi import FastAPI

from fee_track.log import setup_logging

setup_logging()

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app")
