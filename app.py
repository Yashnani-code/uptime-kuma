import os

from flask import Flask, jsonify
from twilio.rest import Client


app = Flask(__name__)


def get_numbers():
    numbers = os.getenv("TWILIO_TO_NUMBERS", "")

    return [
        number.strip()
        for number in numbers.split(",")
        if number.strip()
    ]


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "UP"
    }), 200


@app.route("/trigger-calls", methods=["GET", "POST"])
def trigger_call():

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")

    numbers_to_call = get_numbers()

    if not account_sid:
        return jsonify({
            "error": "TWILIO_ACCOUNT_SID is not configured"
        }), 500

    if not auth_token:
        return jsonify({
            "error": "TWILIO_AUTH_TOKEN is not configured"
        }), 500

    if not from_number:
        return jsonify({
            "error": "TWILIO_FROM_NUMBER is not configured"
        }), 500

    if not numbers_to_call:
        return jsonify({
            "error": "TWILIO_TO_NUMBERS is not configured"
        }), 500

    client = Client(
        account_sid,
        auth_token
    )

    call_sids = []

    for number in numbers_to_call:

        call = client.calls.create(

            twiml="""
            <Response>
                <Say>
                    Uptime Kuma alert.
                    The monitored service is down.
                    Please check the server.
                </Say>
            </Response>
            """,

            to=number,

            from_=from_number
        )

        call_sids.append(call.sid)

    return jsonify({

        "message": "Calls initiated",

        "call_sids": call_sids

    }), 200


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
