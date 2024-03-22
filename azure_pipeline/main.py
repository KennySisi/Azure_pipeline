import os
from fastapi import FastAPI

from azure.applicationinsights import AzureApplicationInsights

app = FastAPI()

instrumentation_key = os.environ.get('INSTRUMENTATION_KEY')

if instrumentation_key:
    azure_app_insights = AzureApplicationInsights(instrumentation_key=instrumentation_key)
    azure_app_insights.init_app(app)

@app.get("/")
def rootFunction():
    return "Hello, visitor new deploy triggered"


@app.get("/Add/{number1}")
def add_two(number1):
    return {f"backend2: Your input is: {number1}"}
