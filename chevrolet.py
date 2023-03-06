"""Importing necessary modules"""
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import date
import datetime
import sys
import requests
from constants import CHERVO_HEADERS, CHERVO_URL, CHERVO_PARMS, OpenRecall, CHERVOLET
from utils import Myutils

class Chevrolet:
    """ Class for accessing the Ford API and getting vin details"""

    def __init__(self):
        self.session = requests.session()
        self.headers = CHERVO_HEADERS
        self.url = CHERVO_URL
        self.params = CHERVO_PARMS
        self.vin = []
        self.utils = Myutils(CHERVOLET)
        logging.basicConfig(filename=f'{CHERVOLET}_logs_{date.today().strftime("%d_%m_%Y")}.log',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO)
        self.logger_obj = logging.getLogger()
    
    def get_status_info(self, vim_id):
        """
        This function will take data by vehiclein id
        """
        vim_url = self.url.format(VIM_ID=vim_id)
        response = self.session.get(
            url=vim_url, params=self.params, headers=self.headers)

        if response.status_code == 200:
            vim_response = response.json()
            if vim_response['messages'] == ['VEHICLE_INVALID_VIN']:
                self.logger_obj.error("This %s is invalid", vim_id)

            try:
                self.vim_data = vim_response.get('data').get('gfas')
                if len(self.vim_data) == 0:
                    open_recalls = OpenRecall.No
                else:
                    open_recalls = OpenRecall.Yes

            except AttributeError:
                open_recalls = OpenRecall.No

            return open_recalls
        self.logger_obj.error("error while scrapping %s", vim_id)

    def get_vim_data(self, vim_id):
        """This function will take data by vehiclein id"""

        open_recalls = self.get_status_info(vim_id)

        if open_recalls.value:

            for data in self.vim_data:

                name_of_recall = data.get('title')
                if name_of_recall:
                    if ":" in name_of_recall:
                        name_of_recall = name_of_recall.split(':')[1]
                else:
                    name_of_recall = ''

                info = data.get('gfaTexts')
                if info:
                    info = info[0]
                    description = info.get('description', '')
                    safetyrisk = info.get('safetyRisk', '')
                    remedy = info.get('remedy', '')
                else:
                    description = safetyrisk = remedy = ''

                gov_info = data.get('governmentAgencies')
                if gov_info:
                    gov_info = gov_info[0]
                    govt_agency_num = gov_info.get('govtAgencyNum')
                else:
                    govt_agency_num = ''

                vin_status = data.get('vinStatusInfo')
                if vin_status:
                    vin_status = vin_status.get('vinStatus')

                self.utils.recall_csv(open_recalls=open_recalls.name, recall_status=vin_status,
                                      name_of_recall=name_of_recall.strip(),
                                      campaign_nhsta=govt_agency_num.strip(),
                                      date_of_recall_announcement=data.get('validStartDate', ''),
                                      brief_description=description.strip(),
                                      safety_risk=safetyrisk.strip(),
                                      remedy=remedy.strip(), vim_id=vim_id,
                                      time_stamp=datetime.datetime.now()
                                      )
        else:
            self.utils.recall_csv(open_recalls=open_recalls.name, 
                                  vim_id=vim_id,time_stamp=datetime.datetime.now())

    def multi_threading(self, csvfile_name):
        """
         This function is used to create multiple threads to process the data

        """
        self.vin.extend(self.utils.get_vin(csvfile_name))
        self.utils.creating_files()
        with ThreadPoolExecutor() as executor:
            executor.map(self.get_vim_data, self.vin)


if __name__ == "__main__":
    file_name = sys.argv[1]
    chervo = Chevrolet()
    chervo.multi_threading(file_name)
