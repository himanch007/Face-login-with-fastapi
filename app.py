from fastapi import Depends, FastAPI
import uvicorn
from middleware.exception_middleware import catch_exceptions_middleware
from middleware.http_error import Conflict, Unauthorized, http_error_handler
from users.controllers import user
from dependencies.authentication import authentication_dependency
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(docs_url=os.getenv('DOCS_URL'))

@app.get("/")
def index():
    return {"name":"Backend"}



if __name__ == "__main__":
    uvicorn.run(app)


# error handlers
app.add_exception_handler(Unauthorized, http_error_handler)
app.add_exception_handler(Conflict, http_error_handler)


# middleware
# app.middleware('http')(catch_exceptions_middleware)


app.include_router(user.router, prefix="/users", tags=["users"], dependencies=[Depends(authentication_dependency)])
