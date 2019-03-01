# get_thumbnail_from_manifest.py
""" Retrieves thumbnail from Manifest """

import json
from urllib import request, error


def get_thumbnail_from_manifest(unique_id):
    """ Open manifest from URL given id.  Retrieve thumbnail from manifest."""
    thumbnail = ""
    manifest_baseurl = 'https://d1v1nx8kcr1acm.cloudfront.net/'
    try:
        manifest_url = manifest_baseurl + unique_id + '/manifest/index.json'
        manifest = json.load(request.urlopen(manifest_url))
        thumbnail = manifest['thumbnail']['@id']
    except error.HTTPError:
        pass  # If we get a url error, we can't get a thumbnail
    return thumbnail
