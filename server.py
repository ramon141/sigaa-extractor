from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import main
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Credentials(BaseModel):
    username: str
    password: str
    infos: List[str]


@app.get('/')
def index():
    return {
        'message': 'Acesse a página /docs'
    }


@app.post('/get_infos')
def train(credentials: Credentials):
    infos = {
        'main': {},
        'restaurant': {}
    }

    for type in credentials.infos:
        if type == 'main':
            infos['main'] = main.get_main_info(main.driver)
        if type == 'restaurant':
            infos['restaurant'] = main.get_restaurant_info(main.driver)

    return infos
