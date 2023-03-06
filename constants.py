"""
    This file stores all the headers and prams of ford and chevrolet
"""
from enum import Enum


class OpenRecall(Enum):
    """To set the recall value"""
    Yes = True
    No = False


CHERVO_HEADERS = {
    'authority': 'www.chevrolet.com',
    'accept': 'application/json',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'gm.na.requesttype': 'ajax',
    'referer': 'https://www.chevrolet.com/ownercenter/recalls?vin=1GNALDEK2EZ115674',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

CHERVO_URL = 'https://www.chevrolet.com/ownercenter/api/{VIM_ID}/gfas'

CHERVO_PARMS = {
    'cb': '16776038895210.711534244888673',
}

FORD_HEADERS = {
    'Connection': 'keep-alive',
    'Origin': 'https://www.ford.com',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/110.0.0.0 Safari/537.36 '
    'Edg/110.0.1587.56',
}

FORD_PARMS = {
    'vin': '',
    'country': 'usa',
    'langscript': 'LATN',
    'language': 'en',
    'region': 'en-us',
}
FORD_URL = 'https://www.digitalservices.ford.com/owner/api/v2/recalls'

CHERVOLET = "Chevrolet"
FORD = "Ford"

CSV_HEADERS = ['Open_Recalls', 'Recall_status', 'Name_of_Recall',
               'Campaign_NHTSA','Date_of_recall_announcement',
               'Brief_Description', 'Safety_Risk', 'Remedy',
               'Vim_ID', 'Time_Stamp']

OUTPUT_FOLDER = "output_files"
