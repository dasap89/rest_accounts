import json
import pytest
from django.contrib.auth import get_user_model
from .utils import get_token


User = get_user_model()

API_PREFIX = '/api/v1'


@pytest.mark.django_db
def test_that_user_can_login(client):
    email = 'user_one@example.com'

    response = client.post('{}/auth/login'.format(API_PREFIX), {
        'email': email,
        'password': 'test_123'
    })

    assert response.json()['token'] == get_token(email)
    assert response.json()['message'] == 'user {} logged'.format(email)
    assert response.status_code == 200



@pytest.mark.django_db
def test_that_user_cannot_login_with_incorrect_email(client):
    response = client.post('{}/auth/login'.format(API_PREFIX), {
        'email': 'invalid email',
        'password': 'random_password'
    })
    assert response.json()['errors']['email'] == \
           ['Enter a valid email address.']
    assert response.status_code == 400


@pytest.mark.django_db
def test_that_user_cannot_login_when_email_empty(client):
    response = client.post('{}/auth/login'.format(API_PREFIX), {
        'password': 'random_password'
    })
    assert response.json()['errors']['email'] == \
           ['The email field should not be empty']
    assert response.status_code == 400

@pytest.mark.django_db
def test_that_user_cannot_login_when_password_empty(client):
    response = client.post('{}/auth/login'.format(API_PREFIX), {
        'email': 'user_one@example.com',
    })
    assert response.json()['errors']['password'] == \
           ['The password field should not be empty']
    assert response.status_code == 400


@pytest.mark.django_db
def test_that_login_shows_a_error_on_a_incorrect_password(client):
    response = client.post('{}/auth/login'.format(API_PREFIX), {
        'email': 'user_one@example.com',
        'password': 'password'
    })

    assert response.json()['detail'] == 'Invalid credentials'
    assert response.status_code == 403


@pytest.mark.django_db
def test_that_logout_can_delete_a_token(client):
    response = client.delete(
        '{}/auth/logout'.format(API_PREFIX),
        {},
        HTTP_AUTHORIZATION='Token ' + get_token()
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_that_logout_requires_a_valid_token(client):
    response = client.delete(
        '{}/auth/logout'.format(API_PREFIX),
        {},
        HTTP_AUTHORIZATION='Token invalid_token'
    )
    print (response.json())
    assert response.json()['detail'] == 'Invalid token.'
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_can_register_with_valid_data(client):
    email = "new_user@email.com"
    password = "123abc%%%"
    response = client.post(
        '{}/auth/register'.format(API_PREFIX),
        {
            "email": email,
            "password": password
        },
    )

    assert response.status_code == 201
    assert response.json()['email'] == email
    assert User.objects.filter(email=email).exists()


@pytest.mark.django_db
def test_user_cannot_register_with_invalid_data(client):
    response = client.post(
        '{}/auth/register'.format(API_PREFIX),
        {
            "email": "manager_with_invalid_email",
            "password": ""
        },
    )
    assert response.status_code == 400
    assert response.json()['email'] == ['Enter a valid email address.']
    assert response.json()['password'] == ['This field may not be blank.']


@pytest.mark.django_db
def test_user_cannot_register_wo_data(client):
    response = client.post(
        '{}/auth/register'.format(API_PREFIX),
        {},
    )
    assert response.status_code == 400
    assert response.json()['email'] == ['This field is required.']
    assert response.json()['password'] == ['This field is required.']


@pytest.mark.django_db
def test_info_user_returns_data(client):
    user = User.objects.get(email='user_one@example.com')
    response = client.get(
        '{}/auth/info'.format(API_PREFIX),
        HTTP_AUTHORIZATION='Token ' + get_token()
    )

    assert response.status_code == 200
    assert response.json()['email'] == user.email
    assert response.json()['first_name'] == ''
    assert response.json()['last_name'] == ''


@pytest.mark.django_db
def test_info_user_not_returns_data_wo_authorization(client):
    user = User.objects.get(email='user_one@example.com')
    response = client.get(
        '{}/auth/info'.format(API_PREFIX),
    )
    assert response.status_code == 403
    assert response.json()['detail'] == \
           'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_info_user_not_returns_data_with_invalid_token(client):
    user = User.objects.get(email='user_one@example.com')
    response = client.get(
        '{}/auth/info'.format(API_PREFIX),
        HTTP_AUTHORIZATION='Token invalid_token'
    )

    assert response.status_code == 403
    assert response.json()['detail'] == 'Invalid token.'


@pytest.mark.django_db
def test_user_can_change_personal_data(client):
    test = User.objects.get(email="user_one@example.com")
    response = client.put(
        '{}/auth/update'.format(API_PREFIX),
        data=json.dumps({
            "email": "new_email@email.com",
            "first_name": "FirstName",
            "last_name": "LastName",
            "password": "1a2&3456"
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION='Token ' + get_token()
    )

    assert response.status_code == 200
    assert response.json()['detail'] == 'Personal data is changed'
    test_after_changes = User.objects.get(email="new_email@email.com")
    assert test.email != test_after_changes.email
    assert test.first_name != test_after_changes.first_name
    assert test.last_name != test_after_changes.last_name
    assert test.password != test_after_changes.password


@pytest.mark.django_db
def test_user_cannot_change_password_when_pass_is_too_short(client):
    response = client.put(
        '{}/auth/update'.format(API_PREFIX),
        data=json.dumps({
            "password": "1a%"
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION='Token ' + get_token()
    )

    assert response.status_code == 400
    assert 'This password is too short.' in response.json()['password'][0]


@pytest.mark.django_db
def test_user_cannot_change_password_when_pass_with_letters_only(client):
    response = client.put(
        '{}/auth/update'.format(API_PREFIX),
        data=json.dumps({
            "password": "abcdefgh"
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION='Token ' + get_token()
    )

    assert response.status_code == 400
    print(response.json())
    assert response.json()['password'] == \
           ['Password must contain at least 1 digit.']


@pytest.mark.django_db
def test_user_cannot_change_password_when_pass_with_digits_only(client):
    response = client.put(
        '{}/auth/update'.format(API_PREFIX),
        data=json.dumps({
            "password": "12345678"
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION='Token ' + get_token()
    )

    assert response.status_code == 400
    print(response.json())
    assert response.json()['password'] == \
           ['Password must contain at least 1 letter.']


@pytest.mark.django_db
def test_user_cannot_change_password_when_pass_with_spec_chars_only(client):
    response = client.put(
        '{}/auth/update'.format(API_PREFIX),
        data=json.dumps({
            "password": "&&&%%%$$$"
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION='Token ' + get_token()
    )

    assert response.status_code == 400
    print(response.json())
    assert response.json()['password'] == \
           ['Password must contain at least 1 digit.']


@pytest.mark.django_db
def test_user_cannot_change_personal_data_wo_authorization(client):
    response = client.put(
        '{}/auth/update'.format(API_PREFIX),
        data=json.dumps({
            "email": "new_email@email.com",
            "first_name": "FirstName",
            "last_name": "LastName",
            "password": "123456"
        }),
        content_type="application/json",
    )
    assert response.status_code == 403
    assert response.json()['detail'] == 'Authentication creden' \
                                        'tials were not provided.'


@pytest.mark.django_db
def test_user_can_change_just_email(client):
    response = client.put(
        '{}/auth/update'.format(API_PREFIX),
        data=json.dumps({
            "email": "new_email@email.com",
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION='Token ' + get_token(),
    )
    assert response.status_code == 200
    assert response.json()['detail'] == 'Personal data is changed'
