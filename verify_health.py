import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

async def test_health_crud():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Create
        data = {
            "request_time": datetime.now().isoformat(),
            "response_time": datetime.now().isoformat(),
            "difference": 0.5,
            "status": "success"
        }
        print(f"Creating health check: {data}")
        response = await client.post(f"{BASE_URL}/health/checks", json=data)
        if response.status_code != 201:
            print(f"Failed to create: {response.text}")
            return
        
        created = response.json()
        print(f"Created: {created}")
        check_id = created["id"]
        
        # 2. Get All
        print("Fetching all checks...")
        response = await client.get(f"{BASE_URL}/health/checks")
        assert response.status_code == 200
        items = response.json()
        print(f"Found {len(items)} checks")
        assert any(item["id"] == check_id for item in items)
        
        # 3. Get One
        print(f"Fetching check {check_id}...")
        response = await client.get(f"{BASE_URL}/health/checks/{check_id}")
        assert response.status_code == 200
        fetched = response.json()
        assert fetched["id"] == check_id
        
        # 4. Update
        update_data = data.copy()
        update_data["status"] = "updated"
        print(f"Updating check {check_id}...")
        response = await client.put(f"{BASE_URL}/health/checks/{check_id}", json=update_data)
        assert response.status_code == 200
        updated = response.json()
        assert updated["status"] == "updated"
        
        # 5. Delete
        print(f"Deleting check {check_id}...")
        response = await client.delete(f"{BASE_URL}/health/checks/{check_id}")
        assert response.status_code == 204
        
        # 6. Verify Delete
        response = await client.get(f"{BASE_URL}/health/checks/{check_id}")
        assert response.status_code == 404
        print("Verification successful!")

if __name__ == "__main__":
    asyncio.run(test_health_crud())
