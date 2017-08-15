import pytest
import api_helpers as nasa
from common import diff_img_by_urls


@pytest.mark.parametrize('rover', ['curiosity'])
@pytest.mark.parametrize('sol', [1000])
@pytest.mark.parametrize('limit', [10])
def test_sol_earth_equal(rover, sol, limit):
    by_sol = nasa.get_mars_photos(rover, sol=sol)[:limit]
    ed = by_sol[0]['earth_date']
    by_earth_date = nasa.get_mars_photos(rover, earth_date=ed)[:limit]

    for sol_photo, ed_photo in zip(by_sol, by_earth_date):
        assert sol_photo == ed_photo  # check metadata

        # following assertion should never fail as we ensured img_src are
        # the same by comparing metadata (if NASA's static server doesn't
        # give different images for the same urls, of course),
        # so this is only to add some image comparison to the task.
        assert not diff_img_by_urls(sol_photo['img_src'], ed_photo['img_src'])


@pytest.mark.parametrize('rover', ['curiosity'])
@pytest.mark.parametrize('sol', [1000])
@pytest.mark.parametrize('threshold', [0.1])
def test_cam_capacity(rover, sol, threshold):
    cam_cap = {}
    for cam in nasa.get_rover_cameras(rover):
        cam_cap[cam] = len(nasa.get_mars_photos(rover, camera=cam, sol=sol))

    max_cap = max(cam_cap.values())
    low_cap_cams = {cam: cap for cam, cap in cam_cap.items()
                    if cap <= max_cap * threshold}

    assert not low_cap_cams