import logging
from typing import Dict

import requests
api_logger = logging.getLogger('api_logger')
class ResponseValidator:
    @staticmethod
    def validate(response)->Dict:
        try:
            response.raise_for_status()
            api_logger.info(f"{response.json()} Validated")

            return response.json()
        except requests.HTTPError as e:
            api_logger.error(f"HTTP Error: {e}")
            return None
        except ValueError as e:
            api_logger.error(f"Invalid JSON: {e}")
            return None
        except Exception as e:
            api_logger.error(f"An error occurred: {e}")
            return None


def get_and_fetch_response(session, url)->Dict:
    try:
        response = session.get(url)
        api_logger.info(f"GET REQUEST TO {url}")
        return ResponseValidator.validate(response)
    except requests.RequestException as e:
        api_logger.error(f"Request Error: {e}")
        return None


def post_and_fetch_response(session, url, data=None)->Dict:
    headers = {'Content-Type': 'application/json'}
    try:
        response = session.post(url, data=data, headers=headers)
        api_logger.info(f"POST REQUEST TO {url}")
        return ResponseValidator.validate(response)
    except requests.RequestException as e:
        api_logger.error(f"Request Error: {e}")
        return None


def delete_and_fetch_response(session, url)->Dict:
    try:
        response = session.delete(url)
        api_logger.info(f"DELETE REQUEST TO {url}")
        return ResponseValidator.validate(response)
    except requests.RequestException as e:
        api_logger.error(f"Request Error: {e}")
        return None


def put_and_fetch_response(session, url, data=None)->Dict:
    try:
        response = session.put(url, data=data)
        api_logger.info(f"PUT REQUEST TO {url}")
        return ResponseValidator.validate(response)
    except requests.RequestException as e:
        api_logger.error(f"Request Error: {e}")
        return None
