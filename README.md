# BigCommerce Order Update Tool

This Python script is used to update the status of orders in BigCommerce. It also sends a text message to the customer when their order is ready for pickup.

## Requirements

- Python
- `requests` library
- `twilio` library
- `os` and `time` libraries (built-in)

## Setup

1. Create a `creds.py` file in the same directory as `main.py` and add the following variables:
    - `client_id`: Your BigCommerce client ID.
    - `access_token`: Your BigCommerce access token.
    - `store_hash`: Your BigCommerce store hash.
    - `business_name`: Your business name.
    - `address`: Your business address.
    - `hours`: Your business hours.
    - `account_sid`: Your Twilio account SID.
    - `auth_token`: Your Twilio auth token.
    - `TWILIO_PHONE_NUMBER`: Your Twilio phone number.

## Usage

Run `main.py`. The script will prompt you to enter an order ID. After entering the order ID, the script will fetch the order details and display them. You will then be prompted to update the order status. You can choose to set the status to 'Awaiting Pickup', 'Complete', or reset the status.

## Functions

- `get_order_details(order_id)`: Fetches the details of an order from BigCommerce.
- `format_phone(phone_number, mode="Twilio", prefix=True)`: Formats a phone number for either Twilio or Counterpoint configuration.
- `send_text(order_number, name, phone_number)`: Sends a text message to a customer notifying them that their order is ready for pickup.
- `update_order_status()`: Prompts the user to enter an order ID and updates the status of the order.

## Notes

- The script includes a `test_mode` variable. When `test_mode` is set to `True`, the script will use dummy data instead of fetching real order details.
- The script uses the Twilio API to send text messages. You will need a Twilio account and a Twilio phone number to use this feature.
- The script uses the BigCommerce API to fetch and update order details. You will need a BigCommerce account and API credentials to use this feature.
