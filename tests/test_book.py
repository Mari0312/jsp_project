
def test_get_book_info(client):
    from database import Book
    book = Book(name='test_name',
                description='test_description',
                quantity=12,
                ).save()

    response = client.get(f'/books/{book.id}')
    assert response.status_code == 200
    assert response.json() == {'name': 'test_name',
                               'description': 'test_description',
                               'quantity': 12,
                               'id': book.id,
                               'authors': [],
                               'genres': [],
                               'available_quantity': 12,
                               'reviews': []}


def test_create_book(client, authentication_headers):
    response = client.post(
        '/books/', headers=authentication_headers(is_librarian=True),
        json={'name': 'test_name',
              'description': 'test_description',
              'quantity': 12,
              'genres': [],
              'authors': []})
    result = response.json()
    assert response.status_code == 200
    assert 'name' in result
    assert result['name'] == 'test_name'


def test_get_books_info(client, authentication_headers):
    from database import Book
    headers = authentication_headers(is_librarian=True)
    Book(name='test_name', description='test_description', quantity=12).save()
    Book(name='test_name2', description='test_description', quantity=12).save()
    response = client.get(f'/books/', headers=headers)
    assert len(response.json()) == 2


def test_delete_book(client, authentication_headers):
    from database import Book

    headers = authentication_headers(is_librarian=True)
    book = Book(name='test_name2', description='test_description', quantity=12).save()
    response = client.delete(f'/books/{book.id}', headers=headers)
    assert response.json()['message'] == 'Deleted'

    response = client.get(f'/books/', headers=headers)
    assert response.json() == []


def test_update_book(client, authentication_headers):
    from database import Book
    book = Book(name='test_name', description='test_description', quantity=12).save()

    headers = authentication_headers(is_librarian=True)
    resp = client.patch(f'/books/{book.id}',
                        json={
                            'name': 'test_name',
                            'description': 'updated_description',
                            'quantity': 12,
                            'genres': [],
                            'authors': [],
                        },
                        headers=headers)
    result = resp.json()
    assert result['description'] == 'updated_description'


def test_get_genre_info(client):
    from database import Genre
    genre = Genre(name='test_name').save()

    response = client.get(f'/books/genres/{genre.id}')
    assert response.status_code == 200
    assert response.json() == {'name': 'test_name',
                               'id': genre.id,
                               'books': []}


def test_create_genre(client, authentication_headers):
    response = client.post(
        '/books/genres/', headers=authentication_headers(is_librarian=True),
        json={'name': 'test_name'})
    assert response.status_code == 200
    assert response.json()['name'] == 'test_name'
    assert 'id' in response.json()


def test_get_genres_info(client, authentication_headers):
    from database import Genre
    Genre(name='genre 1').save()
    Genre(name='genre 2').save()
    response = client.get(f'/books/genres/', headers=authentication_headers(is_librarian=True))
    assert len(response.json()) == 2


def test_delete_genre(client, authentication_headers):
    from database import Genre

    headers = authentication_headers(is_librarian=True)
    genre = Genre(name='test genre').save()
    deleted_genre_response = client.delete(f'/books/genres/{genre.id}', headers=headers)
    assert deleted_genre_response.json() == {'message': 'Deleted'}


def test_create_review(client, authentication_headers):
    from database import Book

    book = Book(name='test book', description='test_description', quantity='12').save()

    headers = authentication_headers(is_librarian=True)
    resp = client.post(f'/books/{book.id}/reviews/',
                       json={
                           'title': 'Nice one',
                           'rate': 4,
                           'content': '...'
                       },
                       headers=headers)
    result = resp.json()
    assert resp.status_code == 200
    assert 'id' in result


def test_update_review(client, authentication_headers):
    from database import Book
    headers = authentication_headers(is_librarian=False)

    book = Book(name='test book', description='test_description', quantity='12').save()

    resp = client.post(f'/books/{book.id}/reviews/',
                       json={
                           'title': 'Nice one',
                           'rate': 4,
                           'content': '...'
                       },
                       headers=headers)

    resp = client.patch(f'/books/{book.id}/reviews/{resp.json()["id"]}',
                        json={'content': 'new content'},
                        headers=headers)
    result = resp.json()
    assert resp.status_code == 200
    assert result['content'] == 'new content'


def test_delete_review(client, authentication_headers):
    from database import Book
    headers = authentication_headers(is_librarian=False)

    book = Book(name='test book', description='test_description', quantity='12').save()

    resp = client.post(f'/books/{book.id}/reviews/',
                       json={
                           'title': 'Nice one',
                           'rate': 4,
                           'content': '...'
                       },
                       headers=headers)

    resp = client.delete(f'/books/{book.id}/reviews/{resp.json()["id"]}', headers=headers)
    result = resp.json()
    assert resp.status_code == 200
    assert result['message'] == 'Deleted'
