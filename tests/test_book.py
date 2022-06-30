
def test_get_book_info(client):
    response = client.post('/books/',
                       json={
                           "name": "test_name",
                           "text": "lol"
                       },
                       headers=headers
                       )
    resp = client.get(f'/posts/{resp.json["id"]}')
    assert resp.json["name"] == "test_name"


def test_create_post(client, authentication_headers):
    headers = authentication_headers(is_writer=True)
    resp = client.post('/posts/',
                       json={
                           "name": "test_name",
                           "text": "lol"
                       },
                       headers=headers
                       )
    post = Post.get(resp.json["id"])
    assert post.name == "test_name"


def test_get_posts_info(client, authentication_headers):
    headers = authentication_headers(is_writer=True)
    client.post('/posts/',
                json={
                    "name": "test_name",
                    "text": "lol"
                },
                headers=headers
                )
    client.post('/posts/',
                json={
                    "name": "test_name2",
                    "text": "lol"
                },
                headers=headers
                )
    headers = authentication_headers(is_reader=True)
    resp = client.get(f'/posts/', headers=headers)
    assert len(resp.json) == 2


def test_delete_post(client, authentication_headers):
    headers = authentication_headers(is_writer=True)
    client.post('/posts/',
                json={
                    "name": "test_name",
                    "text": "lol"
                },
                headers=headers
                )
    client.post('/posts/',
                json={
                    "name": "test_name2",
                    "text": "lol"
                },
                headers=headers
                )
    resp = client.get(f'/posts/', headers=headers)
    assert len(resp.json) == 2

    delete_post = client.delete(f'/posts/{resp.json[0]["id"]}', headers=headers)
    resp = client.get(f'/posts/', headers=headers)
    assert len(resp.json) == 1


def test_update_post(client, authentication_headers):
    headers = authentication_headers(is_writer=True)
    resp = client.post('/posts/',
                       json={
                           "name": "test_name",
                           "text": "lol"
                       },
                       headers=headers
                       )

    resp = client.put(f'/posts/{resp.json["id"]}',
                      json={
                          "name": "test_name2",
                          "text": "loloo"
                      },
                      headers=headers
                      )

    post = Post.get(resp.json["id"])
    assert post.name == "test_name2"
    assert post.text == "loloo"


