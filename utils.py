import config
import logging
import requests
import traceback
from typing import Optional

logging.basicConfig(filename=config.LOGS_PATH, level=logging.DEBUG)


def get_issuer_jwt() -> Optional[str, None]:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'client_id': config.KEYCLOAK_CLIENT_ID,
        'client_secret': config.KEYCLOAK_CLIENT_SECRET,
        'grant_type': config.KEYCLOAK_GRANT_TYPE[config.CLEINT_CREDITIONAL],
    }

    try:
        response = requests.post(
            url=config.KEYCLOAK_URL,
            headers=headers,
            data=data
        )

        logging.debug(f'Get issuer jwt response: {response}')

        return response.json()['access_token']
    except Exception as e:
        logging.debug(f'error: {e}')
        logging.debug(f'traceback: {traceback.format_exc()}')

    return None


def get_subject_jwt(requested_subject: str) -> Optional[str, None]:
    issuer_jwt = get_issuer_jwt()

    headers = {}
    data = {
        'client_id': config.KEYCLOAK_CLIENT_ID,
        'grant_type': config.KEYCLOAK_GRANT_TYPE[config.TOKEN_EXCHANGE],
        'client_secret': config.KEYCLOAK_CLIENT_SECRET,
        'subject_token': issuer_jwt,
        'requested_subject': requested_subject
    }

    try:
        response = requests.post(
            url=config.KEYCLOAK_URL,
            data=data
        )

        logging.debug(f'Get subject jwt response: {response}')

        return response.json()['access_token']
    except Exception as e:
        logging.debug(f'error: {e}')
        logging.debug(f'traceback: {traceback.format_exc()}')

    return None
