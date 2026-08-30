from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"root": "I'm the root."}


@app.get("/hello")
def hello():
    return {"Hello": "How you doing?"}
