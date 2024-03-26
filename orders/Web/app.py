import os
from pathlib import Path
import yaml

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidTokenError,
    InvalidSignatureError,
    MissingRequiredClaimError
)

from starlette import status
from starlette.middleware.base import (
    RequestResponseEndpoint,
    BaseHTTPMiddleware
)
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from orders.Web.api.auth import decode_and_validate_token


app = FastAPI(
        debug=True,
        openapi_url="/openapi/orders.json",
        docs_url="/docs/orders"
    )

oas_doc = yaml.safe_load(
    (Path(__file__).parent / Path("oas.yaml")).read_text()
)

app.openapi = lambda: oas_doc

class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        if os.getenv("AUTH_ON", "False") != "True":
            request.state.user_id = "test"
            return await call_next(request)
    
        if request.url.path in ["/docs/orders", "/openapi/orders.json"]:
            return await call_next(request)
        
        if request.method == "OPTIONS": # CORS preflight requestは認証をスキップ
            return await call_next(request)
        
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing access token",
                    "body": "Missing access token"
                }
            )
        try:
            auth_token = bearer_token.split(" ")[1].strip() # "Bearer <token>" -> <token>
            token_payload = decode_and_validate_token(auth_token)
        except (
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAlgorithmError,
            InvalidAudienceError,
            InvalidKeyError,
            InvalidTokenError,
            InvalidSignatureError,
            MissingRequiredClaimError
        ) as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": str(error),
                    "body": str(error)
                }
            )
        else:
            request.state.user_id = token_payload["sub"]
            return await call_next(request)

app.add_middleware(AuthorizeRequestMiddleware)        
        
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from orders.Web.api import api

