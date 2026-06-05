import pytest
from httpx import AsyncClient,ASGITransport
from app.main import app
from httpx import ASGITransport, AsyncClient
from unittest.mock import MagicMock
from app.database.database_config import get_db


class FakeProduct:
    def __init__(self, id, name):
        self.id = id
        self.name = name

        
@pytest.mark.asyncio
async def test_get_all_products():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, 
                           base_url="http://127.0.0.1:8000",
                           follow_redirects=True) as client:
        response = await client.get("/products")

        assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_product_success():
    mock_db = MagicMock()
    
    fake_product = FakeProduct(id=2, name="Simple Product")  
    mock_db.query.return_value.filter.return_value.first.return_value = fake_product
    app.dependency_overrides[get_db] = lambda: mock_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000", follow_redirects=True) as client:
        response = await client.get("/products/1")
        
        assert response.status_code == 200
        assert response.json()["id"]==2
    app.dependency_overrides.clear()
