from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from services.auth_service import verifyTokenForUser
from datetime import datetime
class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # if request.url.path in ["/auth/login", "/auth/register", "/docs", "/openapi.json"]:
        #     return await call_next(request)

        # token = request.headers.get("Authorization")

        # if not token:
        #     return JSONResponse(status_code=401, content={"error": "Missing token"})

        # token = token.replace("Bearer ", "")
        # user = verifyTokenForUser(token)

        # if not user:
        #     return JSONResponse(status_code=401, content={"error": "Invalid token"})

        # request.state.user = user
        # timebefore=datetime.now()
        print("route started",datetime.now())


        response = await call_next(request)
    
        timeafter=datetime.now()
        print("route ended",datetime.now())
        print("total time taken = ",timeafter-timebefore)


        return response