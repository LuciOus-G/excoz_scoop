"""
SCOOP PLATFORM ID = E_ESHIER : 21
"""
from pathlib import Path

from fastapi import FastAPI, Request, Response
from tortoise.contrib.fastapi import register_tortoise
import os

BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/'))

app = FastAPI(
    debug=True
)

@app.get('/test')
def test():
    return {
        "bapuck2baju partai": "bangsat kau",
        "dj kecil": "okey lesgooo"
    }


# set up custom error handling
class UnicornException(Exception):
    def __init__(self, developer_message: str, user_message: str, status_code=500):
        self.developer_message = developer_message
        self.user_message = user_message
        self.status_code = status_code


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "developer_message": exc.developer_message,
            "user_message": exc.user_message
        },
    )

from eshier_scoop.utils import settings
#tortoise setting
TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URI},
    "apps": {
        "models": {
            "models": [
                'eshier_scoop.organizations.models',
                'eshier_scoop.users.models',
                'eshier_scoop.orders.models',
                "aerich.models",
                'eshier_scoop.items.models',
            ],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    db_url=settings.DATABASE_URI,
    generate_schemas=True,
    modules={
        'models': [
            'eshier_scoop.organizations.models',
            'eshier_scoop.users.models',
            'eshier_scoop.orders.models',
            "aerich.models",
            'eshier_scoop.items.models',
        ]
    }
)

# SUB-SESSION : g
from contextvars import ContextVar, Token
from typing import Any, Dict, Optional
from starlette.types import ASGIApp, Receive, Scope, Send


class Globals:
    __slots__ = ("_vars", "_reset_tokens")

    _vars: Dict[str, ContextVar]
    _reset_tokens: Dict[str, Token]

    def __init__(self) -> None:
        object.__setattr__(self, '_vars', {})
        object.__setattr__(self, '_reset_tokens', {})

    def reset(self) -> None:
        for _name, var in self._vars.items():
            try:
                var.reset(self._reset_tokens[_name])
            # ValueError will be thrown if the reset() happens in
            # a different context compared to the original set().
            # Then just set to None for this new context.
            except ValueError:
                var.set(None)

    def _ensure_var(self, item: str) -> None:
        if item not in self._vars:
            self._vars[item] = ContextVar(f"globals:{item}", default=None)
            self._reset_tokens[item] = self._vars[item].set(None)

    def __getattr__(self, item: str) -> Any:
        self._ensure_var(item)
        return self._vars[item].get()

    def __setattr__(self, item: str, value: Any) -> None:
        self._ensure_var(item)
        self._vars[item].set(value)


class GlobalsMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # g.reset()
        await self.app(scope, receive, send)


from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
    # TODO ip fe stag
    # TODO ip fe prod
    # TODO ip local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(GlobalsMiddleware)
g = Globals()

# END SUB-SESSION : g

def eshier_routes():
    from eshier_scoop.auth.apis import auth_r
    from eshier_scoop.users.apis import user_r
    from eshier_scoop.items.apis import items_r
    app.include_router(auth_r)
    app.include_router(user_r)
    app.include_router(items_r)

eshier_routes()