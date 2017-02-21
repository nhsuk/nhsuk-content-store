import base64
import json

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def make_request(url_part):
    """
    Makes a request to GitHub to get the live content.
    """
    if not settings.GITHUB_OAUTH_TOKEN:
        raise ImproperlyConfigured(
            'Please set GITHUB_OAUTH_TOKEN in your settings'
        )

    url = settings.IMPORT_URL_FORMAT.format(url_part=url_part)
    response = requests.get(url, headers={
        'Authorization': 'token %s' % settings.GITHUB_OAUTH_TOKEN
    })
    assert response.ok, response.content

    return json.loads(response.content.decode('utf-8'))


def get_data_from_remote(url_part, is_json=False, is_file=False):
    """
    Returns the data related to the url identified by `url_part`.
    If `is_json` == True, it returns the json representation.
    If `is_file` == True it does not attempt to decode the content.
    """
    response_content = make_request(url_part)
    data = base64.b64decode(response_content['content'])

    if not is_file:
        data = data.decode('utf-8')

    if is_json:
        data = json.loads(data)
    return data


def get_list_of_children_from_remote(url_part):
    """
    Returns the subfolders of an item (e.g. conditions, symptoms).
    url_part can be either a string e.g. 'conditions' relative to
    the content folder or it can be an absolute url_part starting
    from /content e.g. /content/conditions/hernia.
    """
    if not url_part.startswith('/content'):
        url_part = '/content/%s' % url_part

    data = make_request(url_part)
    return [item['name'] for item in data if item['type'] == 'dir']
