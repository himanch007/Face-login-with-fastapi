from fastapi import Depends, FastAPI
import uvicorn
from middleware.exception_middleware import catch_exceptions_middleware
from middleware.http_error import Unauthorized, http_error_handler
from users.routes import user
from dependencies.authentication import authentication_dependency


app = FastAPI(docs_url='/docs')

@app.get("/")
def index():
    return {"name":"Backend"}



if __name__ == "__main__":
    uvicorn.run(app)


# error handlers
app.add_exception_handler(Unauthorized, http_error_handler)


# middleware
# app.middleware('http')(catch_exceptions_middleware)


app.include_router(user.router, prefix="/users", tags=["users"], dependencies=[Depends(authentication_dependency)])