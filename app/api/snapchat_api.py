import json

from app import Config
from app.utils import hashing, api
from app.utils.auth import OAuthHandler


class SnapchatAPI:
    SCHEMAS = {
        "email": "EMAIL_SHA256",
        "mobile": "MOBILE_AD_ID_SHA256",
        "phone": "PHONE_SHA256"
    }
    oauth_handler = OAuthHandler()

    @staticmethod
    def add_users_to_segment(segment_id, schema_name, identifiers):
        session = SnapchatAPI.oauth_handler.get_session_with_headers()
        url = f"{Config.BASE_URL}/segments/{segment_id}/users"
        payload = SnapchatAPI._prepare_add_users_to_segment_payload(segment_id, SnapchatAPI.SCHEMAS[schema_name],
                                                                    identifiers)
        return api.post_and_fetch_response(session, url, data=payload)

    @staticmethod
    def add_new_segment(segment_name, description, retention_days):
        session = SnapchatAPI.oauth_handler.get_session_with_headers()
        url = f"https://adsapi.snapchat.com/v1/adaccounts/{Config.AD_ACCOUNT_ID}/segments"
        payload = SnapchatAPI._prepare_add_segment_payload(segment_name, description, retention_days)
        response = api.post_and_fetch_response(session, url, data=payload)
        return SnapchatAPI._extract_segment_info(response)

    @staticmethod
    def fetch_all_segments():
        session = SnapchatAPI.oauth_handler.get_session_with_headers()
        url = f"https://adsapi.snapchat.com/v1/adaccounts/{Config.AD_ACCOUNT_ID}/segments"
        response_payload = api.get_and_fetch_response(session, url)
        if response_payload['request_status'] == "SUCCESS":
            return SnapchatAPI._extract_segments_info_list(response_payload)
        return []

    @staticmethod
    def get_segment(segment_id):
        session = SnapchatAPI.oauth_handler.get_session_with_headers()
        url = f"https://adsapi.snapchat.com/v1/segments/{segment_id}"
        response_payload = api.get_and_fetch_response(session, url)
        if response_payload['request_status'] == "SUCCESS":
            return SnapchatAPI._extract_segment_info(response_payload)
        return None

    @staticmethod
    def delete_segment(segment_id):
        session = SnapchatAPI.oauth_handler.get_session_with_headers()
        url = f"https://adsapi.snapchat.com/v1/segments/{segment_id}"
        return api.delete_and_fetch_response(session, url)

    @staticmethod
    def update_segment(segment_id, segment_name, description, retention_days):
        session = SnapchatAPI.oauth_handler.get_session_with_headers()
        url = f"https://adsapi.snapchat.com/v1/adaccounts/{Config.AD_ACCOUNT_ID}/segments"
        payload = SnapchatAPI._prepare_update_segment_payload(segment_id, segment_name, description, retention_days)
        return api.put_and_fetch_response(session, url, data=payload)

    @staticmethod
    def _prepare_add_segment_payload(segment_name, description, retention_days):
        return json.dumps({
            "segments": [
                {
                    "name": f"{segment_name}",
                    "description": f"{description}",
                    "source_type": "FIRST_PARTY",
                    "retention_in_days": retention_days,
                    "ad_account_id": f"{Config.AD_ACCOUNT_ID}"
                }
            ]
        })

    @staticmethod
    def _prepare_update_segment_payload(segment_id, segment_name, description, retention_days):
        return json.dumps({
            "segments": [
                {
                    "id": f"{segment_id}",
                    "name": f"{segment_name}",
                    "organization_id": f"{Config.ORGANIZATION_ID}",
                    "description": f"{description}",
                    "retention_in_days": retention_days
                }
            ]
        })

    @staticmethod
    def _prepare_add_users_to_segment_payload(segment_id, schema, identifiers):
        return json.dumps({"users": [{"id": f"{segment_id}", "schema": [schema],
                                      "data": [[hashing.hash_identifier(identifier)] for identifier in identifiers]}]})

    @staticmethod
    def _extract_segments_info_list(response_payload):
        return [{'id': segment['segment']['id'],
                 'name': segment['segment']['name'],
                 'description': segment['segment']['description'],
                 'retention_days': segment['segment']['retention_in_days'],
                 'upload_status': segment['segment']['upload_status'],
                 'approx_users': segment['segment']['approximate_number_users'],
                 'targetable_status': segment['segment']['targetable_status'],
                 'status': segment['segment']['status'],

                 } for segment in
                response_payload['segments']]

    @staticmethod
    def _extract_segment_info(response_payload):
        segment = response_payload['segments'][0]['segment']

        return {'id': segment['id'], 'name': segment['name'],
                'description': segment['description'],
                'retention_days': segment['retention_in_days'],
                'upload_status': segment['upload_status'],
                'approx_users': segment['approximate_number_users'],
                'targetable_status': segment['targetable_status']
                }

