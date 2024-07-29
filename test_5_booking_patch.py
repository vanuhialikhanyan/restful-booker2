import allure
import pytest
import requests

import test_1_booking_token
import test_2_booking_post


@allure.feature('Booking Feature')
@allure.suite('Partial Update Booking Suite')
@allure.title('Test Partial Update Booking')
@allure.description('Test to partially update a booking and verify the response.')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_partial_update_booking():
    body = {
        "firstname": "James",
        "lastname": "Brown"
    }
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
               'Cookie': f'token={test_1_booking_token.my_token}'}

    with allure.step('Send PATCH request to partially update a booking'):
        response = requests.patch(
            f'https://restful-booker.herokuapp.com/booking/{test_2_booking_post.my_bookingid}',
            json=body,
            headers=headers
        )

    with allure.step('Verify response status code is 200'):
        assert response.status_code == 200, f'Expected status code 200 but got {response.status_code}'

    response_data = response.json()

    with allure.step('Verify firstname is updated correctly'):
        assert body['firstname'] == response_data[
            'firstname'], f"Expected firstname to be {body['firstname']}, but got {response_data['firstname']}"

    with allure.step('Verify lastname is updated correctly'):
        assert body['lastname'] == response_data[
            'lastname'], f"Expected lastname to be {body['lastname']}, but got {response_data['lastname']}"

    with allure.step('Verify totalprice is present in response'):
        assert 'totalprice' in response_data, "'totalprice' key not found in response"

    with allure.step('Verify depositpaid is present in response'):
        assert 'depositpaid' in response_data, "'depositpaid' key not found in response"

    with allure.step('Verify bookingdates is present in response'):
        assert 'bookingdates' in response_data, "'bookingdates' key not found in response"

    with allure.step('Verify checkin date is present in bookingdates'):
        assert 'checkin' in response_data['bookingdates'], "'checkin' key not found in 'bookingdates'"

    with allure.step('Verify checkout date is present in bookingdates'):
        assert 'checkout' in response_data['bookingdates'], "'checkout' key not found in 'bookingdates'"

    with allure.step('Verify additionalneeds is present in response'):
        assert 'additionalneeds' in response_data, "'additionalneeds' key not found in response"

    with allure.step('Printing response'):
        allure.attach(response.text, 'Response', allure.attachment_type.JSON)

@allure.feature('Booking Feature')
@allure.suite('Partial Update Booking Suite')
@allure.title('Test Negative Partial Update Booking with Invalid Token')
@allure.description('Test to verify response when partially updating a booking with an invalid token.')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_negative_partial_update_booking():
    body = {
        "firstname": "James",
        "lastname": "Brown"
    }
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Cookie': 'token=12312312'}

    with allure.step('Send PATCH request with invalid token to partially update a booking'):
        response = requests.patch(
            f'https://restful-booker.herokuapp.com/booking/{test_2_booking_post.my_bookingid}',
            json=body,
            headers=headers
        )

    with allure.step('Verify response status code is 403'):
        assert response.status_code == 403, f'Expected status code 403 but got {response.status_code}'


@pytest.mark.regression
@allure.feature('Booking Feature')
@allure.suite('Partial Update Booking Suite')
@allure.title('Test Negative Partial Update Booking without Token')
@allure.description('Test to verify response when partially updating a booking without a token.')
@allure.severity(allure.severity_level.CRITICAL)
def test_negative_partial_update_without_token_booking():
    body = {
        "firstname": "James",
        "lastname": "Brown"
    }
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    with allure.step('Send PATCH request without token to partially update a booking'):
        response = requests.patch(
            f'https://restful-booker.herokuapp.com/booking/{test_2_booking_post.my_bookingid}',
            json=body,
            headers=headers
        )

    with allure.step('Verify response status code is 403'):
        assert response.status_code == 403, f"Expected status code 403 but got {response.status_code}"