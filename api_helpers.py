import urllib.parse
import requests


API_KEY = '1I6QqnLuiJ4mPggQ3M0HeHNTnvsCgvgT3oydX6sG'

API_URLS = {
    'main': 'https://api.nasa.gov/',
    'mars_photos': '/mars-photos/api/v1/rovers/{rover}/photos',
    'mars_manifests': '/mars-photos/api/v1/manifests/{rover}',
}


def get(url, params=None, **kwargs):
    params = params or {}
    params['api_key'] = API_KEY
    url = urllib.parse.urljoin(API_URLS['main'], url)

    resp = requests.get(url, params=params, **kwargs)
    data = resp.json()

    if 'errors' in data:
        raise RuntimeError('error getting %s: %s' % (resp.url, data['errors']))

    return data


def get_mars_photos(rover, camera=None, sol=None, earth_date=None, page=None):
    assert not (sol and earth_date), "Can't use sol and earth_date together"
    params = dict(camera=camera, page=page)

    if earth_date:
        params['earth_date'] = earth_date
    else:
        params['sol'] = sol

    return get(API_URLS['mars_photos'].format(rover=rover), params)['photos']


def get_manifest_rover_cameras(rover):
    data = get(API_URLS['mars_manifests'].format(rover=rover))
    return sorted(set(cam for sol_photos in data['photo_manifest']['photos']
                      for cam in sol_photos['cameras']))


def get_rover_cameras(rover):
    sol_limit = 10
    for sol in range(sol_limit):
        for photo in get_mars_photos(rover, sol=sol, page=1):
            return [c['name'] for c in photo['rover']['cameras']]
    else:
        raise RuntimeError('no photos for the first %d sols from %s. '
                           % (sol_limit, rover) + "Can't get cameras")
