from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import yaml

app = FastAPI(
        debug=True,
        openapi_url="/openapi/orders.json",
        docs_url="/docs/orders"
    )

oas_doc = yaml.safe_load(
    (Path(__file__).parent / Path("oas.yaml")).read_text()
)

app.openapi = lambda: oas_doc

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from orders.Web.api import api

