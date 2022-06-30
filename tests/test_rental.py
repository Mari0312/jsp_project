from datetime import datetime


def test_get_rental_info(client, authentication_headers):
    from database import Rental, User
    user = User(
        first_name='John',
        last_name='Connor',
        birthday='2022-06-29',
        address='Lviv',
        phone_number='380972879503',
        email='123',
        password='testpass',
        is_librarian=True,
    ).save()

    rental = Rental(name='test_name',
                    issue_date=datetime.fromisoformat('2022-07-01').date(),
                    return_date=None,
                    user_id=user.id,
                    ).save()

    response = client.get(f'/rentals/{rental.id}', )
    assert response.status_code == 200
    assert response.json()['name'] == 'test_name'
    assert response.json()['books'] == []


def test_create_rental(client, authentication_headers):
    response = client.post(
        '/rentals/', headers=authentication_headers(is_librarian=True),
        json={'name': 'test_name',
              'issue_date': '2022-07-01T12:12:12',
              'books': []})
    assert response.status_code == 200
    assert response.json()['books'] == []


def test_get_rentals_info(client, authentication_headers):
    from database import Rental, User
    user = User(
        first_name='John',
        last_name='Connor',
        birthday='2022-06-29',
        address='Lviv',
        phone_number='380972879503',
        email='123',
        password='testpass',
        is_librarian=True,
    ).save()

    Rental(name='test_name',
           issue_date=datetime.fromisoformat('2022-07-01').date(),
           return_date=None,
           user_id=user.id).save()

    Rental(name='test_name2',
           issue_date=datetime.fromisoformat('2022-07-02').date(),
           return_date=None,
           user_id=user.id).save()
    response = client.get(f'/rentals/', headers=authentication_headers())
    assert len(response.json()) == 2


def test_close_rental(client, authentication_headers):
    response = client.post(
        '/rentals/', headers=authentication_headers(is_librarian=True),
        json={'name': 'test_name',
              'issue_date': '2022-07-01T12:12:12',
              'books': []})

    rental_id = response.json()['id']
    headers = authentication_headers(is_librarian=True)
    resp = client.post(f'/rentals/{rental_id}/close', headers=headers)
    assert resp.json()['return_date']
