import asyncio
import httpx

async def fetch(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=('Mập', 'Mập khùng'))
        return response

async def main():
    urls = [f"http://localhost:5000/login" for _ in range(1)]  # Replace with your actual URLs
    tasks = [asyncio.create_task(fetch(url)) for url in urls]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response.status_code)  # Access response data as needed

asyncio.run(main())