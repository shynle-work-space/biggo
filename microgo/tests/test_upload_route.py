import asyncio
import httpx

async def login():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:5000/login", auth=('Mập', 'Mập khùng'), timeout=None)
        return response

async def upload(token, file_path):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        if file_path is not None:
            files = {"data": open(file_path, "rb")}
            response = await client.post("http://localhost:5000/upload", headers=headers, files=files, timeout=None)
            return response
        else:
            response = await client.post("http://localhost:5000/upload", headers=headers, timeout=None)
            return response


async def stress_test(num):
    async def upload_sucess():
        login_response = await login()
        token = login_response.json().get('token')
        upload_resp = await upload(token, file_path=None)
        file_path = './assets/pizza.webp'
        upload_resp = await upload(token, file_path=file_path)
        return upload_resp
    
    tasks = [asyncio.create_task(upload_sucess()) for _ in range(num)]

    responses = await asyncio.gather(*tasks)
    return responses


import pytest

@pytest.mark.asyncio
async def test_upload_failure():
    login_response = await login()
    token = login_response.json().get('token')
    upload_resp = await upload(token, file_path=None)
    
    assert upload_resp.status_code == 500
    assert upload_resp.text == 'Upload file is missing'

@pytest.mark.asyncio
async def test_upload_success():
    login_response = await login()
    token = login_response.json().get('token')
    upload_resp = await upload(token, file_path=None)
    file_path = './assets/pizza.webp'
    upload_resp = await upload(token, file_path=file_path)
    
    assert upload_resp.status_code == 201
    assert upload_resp.json().get('fs_id') is not None

@pytest.mark.asyncio
async def test_upload_success_stress():
    responses = await stress_test(20)
    for resp in responses:
        assert resp.status_code == 201
        assert resp.json().get('fs_id') is not None


if __name__ == '__main__':
    asyncio.run(stress_test(20))