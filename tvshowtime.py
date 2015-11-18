import json
import random
import string
import urllib.request
from urllib.request import urlopen
from urllib.parse import urlencode
from xml.etree import ElementTree


def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# fixme make decorator compatible with multiple arguments
def check_token_decorator(func):
    def inner(self):
        if not self.token:
            self.__prompt_authenticate()
        else:
            inner(self)

    return inner


class TvShowTime:
    """ This class is a utility class to connect to the TvShowTime API

    Simply enter your auth infos and use the method : 'make_tvshowtime_request'
    """

    base_url = "https://api.tvshowtime.com/v1"
    base_url_tvdb = "http://thetvdb.com/api/GetSeries.php/api/GetSeries.php"

    def __init__(self, token=None):
        self.client_id = None
        self.client_secret = None
        self.user_agent = None
        self.token = token

        self.device_code = ''

        if not token:
            self.__prompt_authenticate()

    @staticmethod
    def __prompt_authenticate():
        print("Please authenticate . . . . ")
        print("Call the method authenticate with 'client_id', 'client_secret' and 'user_agent'")
        print("The token will automatically be saved, no need to create a new instance!")
        print

    def generate_token(self, client_id, client_secret, user_agent):
        # Save the keys
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

        # Make authentication
        self.__make_step_1()
        self.__make_step_2()

    def __make_tvst_post(self, url, data):
        f = urllib.request.Request(url)
        f.add_header('User-Agent', self.user_agent)

        res = urllib.urlopen(f, data)  # Specifying the data argument transform makes a POST request instead of GET
        return json.load(res)

    def __make_step_1(self):
        step_1_url = "https://api.tvshowtime.com/v1/oauth/device/code?"
        step_1_parameters = urlencode({"client_id": self.client_id})

        step_1_dict = self.__make_tvst_post(step_1_url, step_1_parameters)

        # Print the authentification url and user code
        print("//////////////////////////")
        print("///   AUTHENTICATION   ///")
        print("//////////////////////////")
        print()
        print("Please go to this url : " + step_1_dict.get('verification_url', ''))
        print("And enter this code : " + step_1_dict.get('user_code', 'ERROR'))
        print()
        device_code = step_1_dict.get('device_code', '')

        if device_code is '':
            raise Exception('No DEVICE_CODE . . . error somewhere! ^_^')

        # ok_dialog = dialog.Dialog()
        # ok_dialog.make_ok_dialog("Click 'Ok' when authenticated on TvShowTime")
        input("Press Enter to continue...")

        self.device_code = device_code

    def __make_step_2(self):
        step_2_url = "https://api.tvshowtime.com/v1/oauth/access_token"
        step_2_parameters = urlencode({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.device_code
        })
        step_2_dict = self.__make_tvst_post(step_2_url, step_2_parameters)
        token = step_2_dict.get('access_token', '')

        if token is '':
            raise Exception('No TOKEN . . . error somewhere! ^_^')

        self.token = token
        print("Token = " + token)
        print()

    # fixme make decorator compatible with multiple arguments
    def make_tvshowtime_request(self, method, parameters):
        # Add token & encode parameters
        parameters['access_token'] = self.token
        encoded_parameters = urlencode(parameters)

        # Make the url
        url = self.base_url + "/" + method + "?" + encoded_parameters
        res = urlopen(url)
        res_string = res.read().decode()
        return json.loads(res_string)

    def _get_tvdb_serie_id(self, tv_show_name):
        # Create and encode parameters
        parameters = {
            'seriesname': tv_show_name
        }
        encoded_parameters = urlencode(parameters)

        # Make the url
        url = self.base_url_tvdb + "?" + encoded_parameters

        # Make request
        response = urllib.request.urlopen(url)

        # Parse response
        response_tree = ElementTree.parse(response).getroot()
        if response_tree.find('Series/seriesid') is not None:
            return response_tree.find('Series/seriesid').text  #serie_id
        else:
            return None

    def get_last_aired_episode(self, tv_show_name):
        serie_id = self._get_tvdb_serie_id(tv_show_name)

        if serie_id is not None:
            parameters = {
                'show_id': serie_id
            }

            response = self.make_tvshowtime_request("show", parameters)
            last_aired = response['show']['last_aired']
            return last_aired
        else:
            return None

    def test(self, test_arg):
        return self._get_tvdb_serie_id(test_arg)