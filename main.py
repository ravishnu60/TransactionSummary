from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Union
from google import genai
from google.genai import types
from settings.config import secrets
import pathlib, json, datetime

app = FastAPI(
    title="Transaction Summary API",
    description="API for summarizing transactions",
    version="1.0.0",
)

class ResponseSchema(BaseModel):
    status: bool
    message: str
    data: Union[str, dict] = None
    model_metrics: dict = None

def time_taken(seconds):
    minutes, seconds = divmod(seconds, 60)
    minutes = f"0{int(minutes)}" if minutes < 10 else int(minutes)
    seconds = f"0{int(seconds)}" if seconds < 10 else int(seconds)
    return f"{(minutes)}:{seconds}"

@app.post('/summary')
async def summarize_transactions(file: UploadFile = File(...)):
    started= datetime.datetime.now()
    """
    Endpoint to summarize transactions from an uploaded file.
    """
    client = genai.Client(api_key=secrets.google_key)
    file_bytes= types.Part.from_bytes( data=file.file.read(), mime_type='application/pdf' )

    prompt = '''
    You are a skilled financial analyst with extensive experience in processing and summarizing transaction data for various financial statements.
    Please analyze the statement and extract the following key insights:

    Statement Period: From which date to which date does the statement span?
    Opening Balance and Closing Balance
    Total Income: Sum of all credited amounts
    Total Expense: Sum of all debited amounts
    Net Savings: (Total Income - Total Expense)
    Top Income Sources: List categories or descriptions from where most income was received top  5
    Top Spending Categories: Where the most money was spent (e.g., Rent, Shopping, Food, etc.) top 5
    Monthly Summary: top 5 months highest total income and highest total expense with how much percentage compare to other months.

    Output Format: No code block, just JSON format with keys as mentioned above.

    '''
    try:
        response = client.models.generate_content(
        model=secrets.modal_name,
        contents=[file_bytes, prompt])
        res= response.text
    except Exception as e:
        return ResponseSchema(status=False, message="Error processing the file", data=str(e), model_metrics={})
    # res= "```json\n{\n    \"Statement Period\": {\n        \"startDate\": \"10/11/2018\",\n        \"endDate\": \"02/01/2019\"\n    },\n    \"Balances\": {\n        \"openingBalance\": 80560.26,\n        \"closingBalance\": 83041.89\n    },\n    \"Summary\": {\n        \"totalIncome\": 135400.96,\n        \"totalExpense\": 132919.33,\n        \"netSavings\": 2481.63\n    },\n    \"Top Income Sources\": {\n        \"Funds Transfer In\": 82633.46,\n        \"Salary\": 52230.0,\n        \"Interest\": 537.0,\n        \"Food & Dining Refunds\": 150.5,\n        \"Transportation Refunds\": 8.46,\n        \"Shopping/General Refunds\": 1.0\n    },\n    \"Top Spending Categories\": {\n        \"Personal Transfer Out\": 30279.0,\n        \"Transportation\": 4350.35,\n        \"Shopping & General\": 3817.07,\n        \"Food & Dining\": 2185.12,\n        \"ATM Withdrawal\": 3600.0,\n        \"Bills & Utilities\": 735.0,\n        \"Google Services\": 199.0,\n        \"Uncategorized Expense\": 28.0\n    },\n    \"Monthly Summary\": [\n        {\n            \"month\": \"2018-11\",\n            \"totalIncome\": 61904.0,\n            \"totalExpense\": 60598.05\n        },\n        {\n            \"month\": \"2018-12\",\n            \"totalIncome\": 72959.96,\n            \"totalExpense\": 71621.28\n        },\n        {\n            \"month\": \"2019-01\",\n            \"totalIncome\": 587.0,\n            \"totalExpense\": 700.0\n        },\n        {\n            \"month\": \"2019-02\",\n            \"totalIncome\": 2600.0,\n            \"totalExpense\": 1184.0\n        }\n    ]\n}\n```"
    time_taken_seconds = (datetime.datetime.now() - started).total_seconds()
    model_metrics = {
        "model": secrets.modal_name,
        "time_taken": time_taken(time_taken_seconds),
        "input_size": str(round(file.size/ 1024, 2))+" KB",  # Size in KB
    }
    try:
        res = res.replace("```json", "").replace("```", "")
        res = json.loads(res)
    except Exception as e:
        return ResponseSchema(status=True, message="Unable to structure the response", data= res, model_metrics=model_metrics)
    return ResponseSchema( status=True, message="Transaction summary generated successfully", data=res, model_metrics=model_metrics)