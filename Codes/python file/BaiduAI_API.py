# -*- coding: utf-8 -*-#
from aip import AipOcr

""" APPID AK SK """
APP_ID = '24255809'
API_KEY = 'x9qV8VCwznzFHCC1ygXwlWgr'
SECRET_KEY = '2CT9KdGkbA9job1e6MPuOmGZ2sokf1e5'


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def Translatephoto(filename):
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # Recognize parameters
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "false"

    # Recognize photos stored locally
    image = get_file_content(filename)
    result = client.basicGeneral(image, options)
    words_result = result['words_result']

    return words_result
