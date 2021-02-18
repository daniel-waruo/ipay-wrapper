import hashlib
import hmac
import json

import urllib3

http = urllib3.PoolManager()


def send_request(data, url, method='POST'):
    """send a request with data to a given url """
    r = http.request(method, url, fields=data)
    try:
        return json.loads(r.data.decode())
    except json.decoder.JSONDecodeError:
        return r.data


def parse_data(data: dict):
    """convert from a dictionary to a list of url parameters"""
    data_string = ""
    for key, val in sorted(data.items()):
        data_string += f"{key}={val}&"
    data_string = data_string[:-1]
    return data_string


def get_hash(string: str, security_key: str):
    """ sign the string with our secret """
    h = hmac.new(
        security_key.encode(),
        msg=string.encode(),
        digestmod=hashlib.sha256
    )
    return h.hexdigest()


def get_hash_for_c2b(
        transaction_id,
        phone,
        email,
        vendor_id,
        callback_url,
        security_key,
        live=True,
):
    live = 1 if live else 0
    data_string = f"{live}{transaction_id}{phone}{email}{vendor_id}{callback_url}"
    h = hmac.new(
        security_key.encode(),
        msg=data_string.encode(),
        digestmod=hashlib.sha1
    )
    return h.hexdigest()
