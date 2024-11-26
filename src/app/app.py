import aiohttp
from fastapi import FastAPI
from influxdb_operation import write_to_influx, read_from_influx

app = FastAPI()


@app.get("/")
async def hello():
    return {"hello"}


@app.get("/fetch-todos")
async def fetch_todos(user_id: int = None):
    url = "https://jsonplaceholder.typicode.com/todos"
    params = {"userId": user_id} if user_id else None

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                write_to_influx(data)
                return {"message": f"{len(data)} saved to Influx db."}
            return {"error": f"An error occurred: {response.status}"}

@app.get("/get-todos")
async def get_todos(user_id: int = None):
    return {f"{read_from_influx(1)}"}
    
  