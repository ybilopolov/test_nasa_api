import io
import requests
import scipy.misc


def get_img(url):
    f = io.BytesIO(requests.get(url).content)
    return scipy.misc.imread(f)


def diff_img_by_urls(img_url1, img_url2):
    img1, img2 = map(get_img, (img_url1, img_url2))
    return sum(abs((img1 - img2).ravel()))
