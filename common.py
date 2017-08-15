import io
import requests
import scipy.misc


def get_img(url):
    """Get image from url as numpy.ndarray"""
    f = io.BytesIO(requests.get(url).content)
    return scipy.misc.imread(f)


def diff_img_by_urls(img_url1, img_url2):
    """Get numerical representation of the absolute difference
    between two images, specified by URLs"""
    img1, img2 = map(get_img, (img_url1, img_url2))
    return sum(abs((img1 - img2).ravel()))
