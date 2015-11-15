import httplib2
from credentials_secret import client_id_showtime, client_secret_showtime, user_agent_showtime
import string
import random
from urllib import urlencode
from pprint import pprint
import urllib2
import json


def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class TvShowTime:
    def __init__(self):
        pass

    def step_1_get_device_code(self, url, data):

        f = urllib2.Request(url)
        f.add_header('User-Agent', user_agent_showtime)

        res = urllib2.urlopen(f, data)  # Specifying the data argument transform makes a POST request instead of GET
        res_dict = json.load(res)

        # Print the authentification url and user code
        print "//////////////////////////"
        print "///   AUTHENTICATION   ///"
        print "//////////////////////////"
        print
        print "Please go to this url : " + res_dict.get('verification_url', '')
        print "And enter this code : " + res_dict.get('user_code', 'ERROR')
        print
        return res_dict.get('device_code', '')


def get_token():
    # Create the http client
    connection = httplib2.Http()

    step_1_url = "https://api.tvshowtime.com/v1/oauth/device/code?"
    step_1_parameters = urlencode({"client_id": client_id_showtime})

    tvst = TvShowTime()
    DEVICE_CODE = tvst.step_1_get_device_code(step_1_url, step_1_parameters)
    if DEVICE_CODE is '':
        raise Exception('No device code . . . error somewhere! ^_^')
    print "Device code = " + DEVICE_CODE


get_token()


