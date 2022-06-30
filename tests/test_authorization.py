def test_register(client):
    response = client.post('/authorization/signup',
                           json={
                               "first_name": "John",
                               "last_name": "Connor",
                               "birthday": "2022-06-29",
                               "address": "lviv",
                               "phone_number": "380972879503",
                               "email": "john@test.com",
                               "password": "testpass",
                           })

    result = response.json()
    assert response.status_code == 200
    assert 'email' in result
    assert result['email'] == 'john@test.com'


def test_user_already_exists(client):
    from database import User

    User(
        first_name="John",
        last_name="Connor",
        birthday="2022-06-29",
        address="Lviv",
        phone_number="380972879503",
        email="john@test.com",
        password='testpass',
    ).save()

    response = client.post('/authorization/signup',
                           json={
                               "first_name": "John",
                               "last_name": "Connor",
                               "birthday": "2022-06-29",
                               "address": "lviv",
                               "phone_number": "380972879503",
                               "email": "john@test.com",
                               "password": "testpass",
                           })
    assert response.status_code == 400
    assert response.json() == {'detail': 'User with this email already exist'}


def test_signup_fails(client):
    response = client.post('/authorization/signup',
                           json={
                               "first_name": "John",
                               "last_name": "Connor",
                               "birthday": "2022-06-29",
                               "address": "lviv",
                               "phone_number": "380972879503",
                               "password": "testpass",
                           })
    result = response.json()
    assert response.status_code == 422
    assert result['detail'][0]['msg'] == 'field required'
    assert result['detail'][0]['loc'] == ['body', 'email']


def test_login(client):
    from database import User
    User(
        first_name="John",
        last_name="Connor",
        birthday="2022-06-29",
        address="Lviv",
        phone_number="380972879503",
        email="john@test.com",
        password='testpass',
    ).save()
    response = client.post('/authorization/login',
                           json={
                               "email": "john@test.com",
                               "password": "testpass",
                           })

    assert 'access_token' in response.json()


def test_user_login_fails(client):
    from database import User
    User(
        first_name="John",
        last_name="Connor",
        birthday="2022-06-29",
        address="Lviv",
        phone_number="380972879503",
        email="john@test.com",
        password='testpass',
    ).save()

    response = client.post('/authorization/login',
                           json={
                               "email": "john@test.com"
                           })
    result = response.json()
    assert response.status_code == 422
    assert result['detail'][0]['msg'] == 'field required'
    assert result['detail'][0]['loc'] == ['body', 'password']


def test_user_correct_password(client):
    from database import User
    User(
        first_name="John",
        last_name="Connor",
        birthday="2022-06-29",
        address="Lviv",
        phone_number="380972879503",
        email="john@test.com",
        password='testpass',
    ).save()
    response = client.post('/authorization/login',
                           json={
                               "email": "john@test.com",
                               "password": "testpass2",
                           })
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}
