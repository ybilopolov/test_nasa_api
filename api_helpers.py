import urllib.parse
import requests
from datetime import datetime, timedelta


API_KEY = '1I6QqnLuiJ4mPggQ3M0HeHNTnvsCgvgT3oydX6sG'

API_URLS = {
    'main': 'https://api.nasa.gov/',
    'mars_rover': '/mars-photos/api/v1/rovers/{rover}',
    'mars_photos': '/mars-photos/api/v1/rovers/{rover}/photos',
    'mars_manifests': '/mars-photos/api/v1/manifests/{rover}',
}

DATE_FORMAT = '%Y-%m-%d'
SECONDS_IN_SOL = 24 * 3600 + 39 * 60 + 35.244


def get(url, params=None, **kwargs):
    """
    Get an url from NASA API extending params with the API_KEY

    Args:
        url (str): API url to get
        params (dict): query parameters for API request
        **kwargs: any additional keyword arguments for requests.get call

    Returns:
        dict: deserialized JSON from API response
    """
    params = params or {}
    params['api_key'] = API_KEY
    url = urllib.parse.urljoin(API_URLS['main'], url)

    resp = requests.get(url, params=params, **kwargs)
    data = resp.json()

    if 'errors' in data:
        raise RuntimeError('error getting %s: %s' % (resp.url, data['errors']))

    return data


def get_mars_photos(rover, camera=None, sol=None, earth_date=None, page=None):
    """
    Get list of all photos (as their metadata) for the given criteria

    Args:
        rover (str): rover name
        camera (str, optional): camera name
        sol (int, optional): sol to get photos on
        earth_date (str, optional): earth date to get photos on (%Y-%d-%m)
        page (int, optional): page number, no pagination if omitted

    Returns:
        list[dict]: list of dicts with photos metadata
    """
    assert not (sol and earth_date), "Can't use sol and earth_date together"
    params = dict(camera=camera, page=page)

    if earth_date:
        params['earth_date'] = earth_date
    else:
        params['sol'] = sol

    return get(API_URLS['mars_photos'].format(rover=rover), params)['photos']


def get_rover_info(rover):
    """Get dict with rover's metadata"""
    return get(API_URLS['mars_rover'].format(rover=rover))['rover']


def get_rover_cameras(rover):
    """Get list of rover's cameras short names"""
    return [c['name'] for c in get_rover_info(rover)['cameras']]


def sol_to_earth_date(rover, sol):
    """
    Convert sol date for specific router to the corresponding earth date

    Args:
        rover (str): rover name
        sol (int): sol (Mars solar days since rover's landing)

    Returns:
        str: earth date formatted as specified by DATE_FORMAT
    """
    landing_date_str = get_rover_info(rover)['landing_date']
    landing_date = datetime.strptime(landing_date_str, DATE_FORMAT)
    new_date = landing_date + timedelta(seconds=sol*SECONDS_IN_SOL)
    return new_date.strftime(DATE_FORMAT)
