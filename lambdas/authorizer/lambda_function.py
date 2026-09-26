import os

EXPECTED_TOKEN = os.environ["API_AUTH_TOKEN"]


def lambda_handler(event, context):
    headers = event.get("headers") or {}

    auth = headers.get("authorization", "")

    # Expect: Bearer <token>
    if not auth.startswith("Bearer "):
        return {
            "isAuthorized": False
        }

    token = auth[7:].strip()

    if token == EXPECTED_TOKEN:
        return {
            "isAuthorized": True,
            "context": {
                "authenticated": True
            }
        }

    return {
        "isAuthorized": False
    }
