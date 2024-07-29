import allure
import pytest
import requests

my_token = None


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('Booking Feature')
@allure.suite('Create Token Booking Suite')
@allure.title('Test Booking Token Creation')
@allure.description('Test to create authentication token for booking API.')
@allure.severity(allure.severity_level.NORMAL)
def test_booking_create_token():
    global my_token
    body = {
        "username": "admin",
        "password": "password123"
    }
    headers = {'Content-Type': 'application/json'}

    with allure.step('Send POST request to create token'):
        response = requests.post(
            'https://restful-booker.herokuapp.com/auth',
            headers=headers,
            json=body
        )

    with allure.step('Verify response status code is 200'):
        assert response.status_code == 200, f'Expected status code 200 but got {response.status_code}'

    with allure.step('Verify "token" is present in response'):
        assert 'token' in response.json(), 'Token not found in response'

    with allure.step('Verify "token" length is greater than 0'):
        assert len(response.json().get('token', '')) > 0, 'Token length is 0'

    # Save the token for later use
    my_token = response.json().get('token')