from datetime import datetime


def test_get_author_info(client):
    from database import Author
    author = Author(
        name="test_name",
        date_of_birth="1984-06-29",
        date_of_death=None,
        biography="test_biography"
    ).save()

    response = client.get(f"/authors/{author.id}")
    assert response.status_code == 200
    assert response.json()['id'] == author.id


def test_create_author(client, authentication_headers):
    response = client.post(
        "/authors/", headers=authentication_headers(is_librarian=True),
        json={"name": "test_name",
              "date_of_birth": "1984-06-29",
              "date_of_death": None,
              "biography": "test_biography"
              })
    assert response.status_code == 200
    created_author = response.json()
    assert created_author['biography'] == 'test_biography'
    assert created_author['books'] == []


def test_get_authors_info(client, authentication_headers):
    from database import Author
    Author(name='test_name', date_of_birth=datetime.fromisoformat('1984-06-29').date(), biography='123').save()
    Author(name='test_name2', date_of_birth=datetime.fromisoformat('1984-06-29').date(), biography='123').save()

    response = client.get(f'/authors/', headers=authentication_headers())
    assert len(response.json()) == 2


def test_update_author(client, authentication_headers):
    from database import Author
    author = Author(
        name="test_name",
        date_of_birth=datetime.fromisoformat('1984-06-29').date(),
        date_of_death=None,
        biography="test_biography"
    ).save()
    headers = authentication_headers(is_librarian=True)
    resp = client.patch(f'/authors/{author.id}',
                        json={"biography": "updated"},
                        headers=headers)
    result = resp.json()
    assert result["biography"] == 'updated'
