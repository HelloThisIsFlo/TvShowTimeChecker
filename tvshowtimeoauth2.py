import httplib2
from credentials_secret import client_id_showtime, client_secret_showtime, user_agent_showtime
import string
import random
from urllib import urlencode
from pprint import pprint
import urllib2
import json
import dialog


def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class TvShowTime:
    def __init__(self):
        pass

    def __make_tvst_post(self, url, data):
        f = urllib2.Request(url)
        f.add_header('User-Agent', user_agent_showtime)

        res = urllib2.urlopen(f, data)  # Specifying the data argument transform makes a POST request instead of GET
        return json.load(res)

    def make_step_1(self):
        step_1_url = "https://api.tvshowtime.com/v1/oauth/device/code?"
        step_1_parameters = urlencode({"client_id": client_id_showtime})

        step_1_dict = self.__make_tvst_post(step_1_url, step_1_parameters)

        # Print the authentification url and user code
        print "//////////////////////////"
        print "///   AUTHENTICATION   ///"
        print "//////////////////////////"
        print
        print "Please go to this url : " + step_1_dict.get('verification_url', '')
        print "And enter this code : " + step_1_dict.get('user_code', 'ERROR')
        print
        device_code = step_1_dict.get('device_code', '')

        if device_code is '':
            raise Exception('No DEVICE_CODE . . . error somewhere! ^_^')

        # ok_dialog = dialog.Dialog()
        # ok_dialog.make_ok_dialog("Click 'Ok' when authenticated on TvShowTime")
        raw_input("Press Enter to continue...")

        return device_code

    def make_step_2(self, device_code):
        step_2_url = "https://api.tvshowtime.com/v1/oauth/access_token"
        step_2_parameters = urlencode({
            "client_id": client_id_showtime,
            "client_secret": client_secret_showtime,
            "code": device_code
        })
        step_2_dict = self.__make_tvst_post(step_2_url, step_2_parameters)
        token = step_2_dict.get('access_token', '')

        if token is '':
            raise Exception('No TOKEN . . . error somewhere! ^_^')

        return token


def main():
    tvst = TvShowTime()
    device_code = tvst.make_step_1()
    token = tvst.make_step_2(device_code)



main()
