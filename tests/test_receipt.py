def test_create_receipt(client, auth_token):
    response = client.post(
        "/api/receipt",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "products": [{"name": "Test Product", "quantity": 2, "price": 50.0}],
            "payment": {"type": "cash", "amount": 200.00},
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 100.0
    assert data["rest"] == 100.0
    assert data["payment"]["type"] == "cash"
    assert len(data["products"]) >= 0
    assert data["products"][0]["total"] == 100.0


def test_list_receipts(client, auth_token):
    response = client.get("/api/receipt?limit=5&offset=0", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = response.json()
    assert "receipts" in data
    assert len(data["receipts"]) <= 5


def test_view_receipt(client, auth_token):
    receipt_response = client.get(f"/api/receipt/1", headers={"Authorization": f"Bearer {auth_token}"})
    link_id = receipt_response.json()["link"].split('/')[-1]
    response = client.get(f"/api/receipt/view/{link_id}")
    assert response.status_code == 200
    assert isinstance(response.text, str)
    assert "Test Product" in response.text


def test_invalid_receipt_creation(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/receipt", json={
        "payment_type": "cash"
    }, headers=headers)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
