import logging
import logging.config

from fastapi import FastAPI

from app.routers import category_routes

# logging.basicConfig(level=logging.DEBUG)
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

app = FastAPI()
app.router.prefix = "/api"
app.router.tags = ["root"]
app.include_router(category_routes.router)


@app.get("/")
def root():
    try:
        raise Exception("Simulated debug error occurred!")
    except Exception as e:
        logging.debug(f"An exception occurred {e}")
        logging.debug("Exception traceback:", exc_info=True)
    return {"message": "Hello, I'm root."}


@app.get("/hello")
def hello():
    return {"Hello": "How you doing?"}


@app.get("/test")
def test_endpoint():
    try:
        result = 1 / 0
        return {"result": result}
    except Exception as e:
        logging.debug(f"An exception occurred {e}")
        logging.debug("Exception traceback:", exc_info=True)
