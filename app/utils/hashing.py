import hashlib


def normalize_email(email):
    return email.strip().lower()


def normalize_phone(phone):
    phone = phone.replace('+', '').replace('-', '').replace(' ', '')
    if phone.startswith('00'):
        phone = phone[2:]
    if phone[0] == '0':
        phone = phone[1:]
    return phone


def normalize_mobile_ad_id(ad_id):
    return ad_id.replace('-', '').lower()


def hash_identifier(identifier):
    return hashlib.sha256(identifier.encode()).hexdigest()
