import allure
import pytest
import requests

my_bookingid = 0

@allure.feature('Booking Feature')
@allure.suite('Create Booking Suite')
@allure.title('Test Create Booking')
@allure.description('Test to create a booking and verify the response.')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_create_booking():
    data = {
        "firstname": "Anna",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    headers = {'Content-Type': 'application/json'}

    with allure.step('Send POST request to create a booking'):
        response = requests.post(
            'https://restful-booker.herokuapp.com/booking',
            json=data,
            headers=headers
        )

    with allure.step('Verify response status code is 200'):
        assert response.status_code == 200, f'Expected Status Code 200, but got {response.status_code}'

    response_data = response.json()

    with allure.step('Verify "bookingid" is present in response'):
        assert "bookingid" in response_data, "The response does not contain 'bookingid'"

    with allure.step('Verify "booking" is present in response'):
        assert "booking" in response_data, "The response does not contain 'booking'"

    response_booking = response_data['booking']

    with allure.step('Verify "firstname" is correct'):
        assert 'firstname' in response_booking, "'firstname' key not found in response"
        assert response_booking['firstname'] == data['firstname'], f"Expected firstname to be {data['firstname']} but got '{response_booking['firstname']}'"

    with allure.step('Verify "lastname" is correct'):
        assert 'lastname' in response_booking, "'lastname' key not found in response"
        assert response_booking['lastname'] == data['lastname'], f"Expected lastname to be {data['lastname']} but got '{response_booking['lastname']}'"

    with allure.step('Verify "totalprice" is correct'):
        assert 'totalprice' in response_booking, "'totalprice' key not found in response"
        assert response_booking['totalprice'] == data['totalprice'], f"Expected totalprice to be {data['totalprice']} but got '{response_booking['totalprice']}'"

    with allure.step('Verify "depositpaid" is correct'):
        assert 'depositpaid' in response_booking, "'depositpaid' key not found in response"
        assert response_booking['depositpaid'] == data['depositpaid'], f"Expected depositpaid to be {data['depositpaid']} but got '{response_booking['depositpaid']}'"

    with allure.step('Verify "bookingdates" is correct'):
        assert 'bookingdates' in response_booking, "'bookingdates' key not found in response"
        assert 'checkin' in response_booking['bookingdates'], "'checkin' key not found in 'bookingdates'"
        assert response_booking['bookingdates']['checkin'] == data['bookingdates']['checkin'], f"Expected checkin to be {data['bookingdates']['checkin']} but got '{response_booking['bookingdates']['checkin']}'"
        assert 'checkout' in response_booking['bookingdates'], "'checkout' key not found in 'bookingdates'"
        assert response_booking['bookingdates']['checkout'] == data['bookingdates']['checkout'], f"Expected checkout to be {data['bookingdates']['checkout']} but got '{response_booking['bookingdates']['checkout']}'"

    with allure.step('Verify "additionalneeds" is correct'):
        assert 'additionalneeds' in response_booking, "'additionalneeds' key not found in response"
        assert response_booking['additionalneeds'] == data['additionalneeds'], f"Expected additionalneeds to be {data['additionalneeds']} but got '{response_booking['additionalneeds']}'"

    with allure.step('Printing response'):
        allure.attach(response.text, 'Response', allure.attachment_type.JSON)

    global my_bookingid
    my_bookingid = response_data['bookingid']