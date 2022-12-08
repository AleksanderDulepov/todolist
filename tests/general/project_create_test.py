

def test_auth_panel(client):
    response=client.get('/admin/login/?next=/admin/')
    assert response.status_code==200