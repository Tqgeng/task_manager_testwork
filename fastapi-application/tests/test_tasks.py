import pytest
from httpx import (
    AsyncClient,
    ASGITransport,
)
import pytest_asyncio
from sqlalchemy import text

from core.models import db_helper
from main import main_app
from .config import (
    auth_register,
    auth_login,
    task,
    task_for_id,
)

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=main_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# @pytest_asyncio.fixture(autouse=True)
# async def clean_db(client):
#     async with db_helper.session_factory() as session:
#         await session.execute(text("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE;"))
#         await session.commit()


@pytest_asyncio.fixture(autouse=True)
async def up_db():
    yield
    await db_helper.dispose()


@pytest_asyncio.fixture
async def auth_headers(client):
    register_data = {
        "email": "testuser@example.com",
        "password": "123",
    }
    await client.post(auth_register(), json=register_data)

    login_data = {
        "username": register_data["email"],
        "password": register_data["password"],
    }
    response = await client.post(auth_login(), data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


async def test_create_task(client, auth_headers):
    response = await client.post(
        task(),
        headers=auth_headers,
        json={"title": "Уроки", "description": "Алгебра"},
    )
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["title"] == "Уроки"
    assert "id" in data


async def test_get_tasks(client, auth_headers):
    await client.post(
        task(),
        headers=auth_headers,
        json={"title": "Гулять", "description": "С собой воду"},
    )

    response = await client.get(task(), headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


async def test_get_task_by_id(client, auth_headers):
    create = await client.post(
        task(),
        headers=auth_headers,
        json={"title": "Помыть посуду", "description": "Без химии"},
    )
    task_id = create.json()["id"]

    response = await client.get(task_for_id(task_id), headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Помыть посуду"


async def test_update_task(client, auth_headers):
    create = await client.post(
        task(),
        headers=auth_headers,
        json={"title": "Купить продукты", "description": "Огурец"},
    )
    task_id = create.json()["id"]

    response = await client.patch(
        task_for_id(task_id),
        headers=auth_headers,
        json={"title": "Купить технику"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Купить технику"


async def test_delete_task(client, auth_headers):
    create = await client.post(
        task(),
        headers=auth_headers,
        json={"title": "Играть", "description": "С друзьями"},
    )
    task_id = create.json()["id"]

    response = await client.delete(task_for_id(task_id), headers=auth_headers)
    assert response.status_code == 200

    response = await client.get(task_for_id(task_id), headers=auth_headers)
    assert response.status_code == 404
