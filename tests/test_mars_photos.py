import logging
import pytest

import api_helpers as nasa
from util import diff_img_by_urls, take, filter_dict


log = logging.getLogger(__name__)

TEST_ROVERS = ['curiosity', 'opportunity', 'spirit']


@pytest.mark.parametrize('rover', TEST_ROVERS)
@pytest.mark.parametrize('sol', [1, 500, 1000])
def test_sol_to_earth_date_conversion(rover, sol):
    earth_date = nasa.sol_to_earth_date(rover, sol)
    photos = nasa.get_mars_photos(rover, sol=sol, page=1)
    if photos:
        assert earth_date == photos[0]['earth_date']
    else:
        log.warning('no photos from %s on sol %d', rover, sol)


@pytest.mark.parametrize('rover', TEST_ROVERS)
@pytest.mark.parametrize('sol', [1000])
@pytest.mark.parametrize('limit', [10])
def test_sol_earth_equal(rover, sol, limit):
    ed = nasa.sol_to_earth_date(rover, sol)
    by_sol = take(limit, nasa.get_mars_photos(rover, sol=sol))
    by_earth_date = take(limit, nasa.get_mars_photos(rover, earth_date=ed))

    for sol_photo, ed_photo in zip(by_sol, by_earth_date):
        assert sol_photo == ed_photo  # check metadata

        # following assertion should never fail as we ensured img_src are
        # the same by comparing metadata (if NASA's static server doesn't
        # give different images for the same urls, of course),
        # so this is only to add some image comparison to the task.
        assert not diff_img_by_urls(sol_photo['img_src'], ed_photo['img_src'])


@pytest.mark.parametrize('rover', TEST_ROVERS)
@pytest.mark.parametrize('sol', [1000])
@pytest.mark.parametrize('threshold', [0.1])
def test_cam_capacity(rover, sol, threshold):
    cam_capacity = {
        cam: len(nasa.get_mars_photos(rover, camera=cam, sol=sol))
        for cam in nasa.get_rover_cameras(rover)
    }
    max_capacity = max(cam_capacity.values())
    is_capacity_low = lambda cap: cap <= max_capacity * threshold
    low_cap_cams = filter_dict(is_capacity_low, cam_capacity)

    assert not low_cap_cams, 'low capacity cameras: %s' % low_cap_cams
