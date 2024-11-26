import aiohttp
from fastapi import FastAPI
from write_influx_db import write_to_influx, read_from_influx

app = FastAPI()

@app.get("/fetch-todos")
async def fetch_todos(user_id: int = None):
    url = "https://jsonplaceholder.typicode.com/todos"
    params = {"userId": user_id} if user_id else None

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return {"todos": data}
            return {"error": f"an error occured: {response.status}"}


@app.get("/get-todos")
async def get_todos(user_id: int = None):
    params = 
    return {f"{read_from_influx(1)}"}