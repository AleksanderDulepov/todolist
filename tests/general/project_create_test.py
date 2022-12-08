

def test_auth_panel(client):
    response=client.get('/admin/')
    assert response.status_code==302