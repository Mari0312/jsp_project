


def test_get_user_info(client, authentication_headers):
    from database import User
    user = User(
        first_name="John",
        last_name="Connor",
        birthday="2022-06-29",
        address="Lviv",
        phone_number="380972879503",
        email="john@test.com",
        password='testpass',
    ).save()

    response = client.get(f"/users/{user.id}", headers=authentication_headers(is_librarian=True))
    assert response.status_code == 200
    assert response.json() == {"first_name": "John",
                               "last_name": "Connor",
                               "birthday": "2022-06-29",
                               "address": "Lviv",
                               "phone_number": "380972879503",
                               "email": "john@test.com",
                               "id": user.id,
                               "rentals": [],
                               "reviews": []}


def test_update_user(client, authentication_headers):
    response = client.patch('/authorization/signup',
                            json={
                                "firs_name": "John",
                                "last_name": "Connor",
                                "birthday": "2022-06-29",
                                "address": "lviv",
                                "phone_number": "380972879503",
                                "password": "testpass",
                            })
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}
