from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def rootFunction():
    return "Hello, visitor"

@app.get("/Add/{number1}")
def add_two(number1):
    return {f"Your input is: {number1}"}