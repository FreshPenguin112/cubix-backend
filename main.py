from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return "Hello from my Deta Micro"
