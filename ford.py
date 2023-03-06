"""Importing necessary modules"""
from concurrent.futures import ThreadPoolExecutor
import logging
import datetime
from datetime import date
import sys
import requests
from utils import Myutils
from constants import FORD_HEADERS, FORD_URL, FORD_PARMS, FORD, OpenRecall

class Ford:
    """ Class for accessing the Ford API and getting vin details"""

    def __init__(self):
        self.session = requests.session()
        self.headers = FORD_HEADERS
        self.url = FORD_URL
        self.params = FORD_PARMS
        self.utils = Myutils(FORD)
        self.vin = []
        self.jdata = ""
        logging.basicConfig(filename=f'{FORD}_logs_{date.today().strftime("%d_%m_%Y")}.log',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO)
        self.logger_obj = logging.getLogger()

    def get_status_info(self, vehiclein):
        """This function is to get the status code of the request"""

        self.params['vin'] = vehiclein

        response = requests.get(
            self.url, params=self.params, headers=self.headers)


        if response.status_code == 200:
            self.jdata = response.json()

            try:
                if self.jdata['recallsCount'] == 0:
                    self.logger_obj.info('No recalls and customer \
                                         satisfaction available for %s', vehiclein)
                    open_recalls = OpenRecall.No
                else:
                    self.logger_obj.info("Recalls and customer satisfaction \
                                         available for %s", vehiclein)
                    open_recalls = OpenRecall.Yes

            except:
                self.logger_obj.error('Invalid vin %s', vehiclein)
                open_recalls = OpenRecall.No

            return open_recalls
        self.logger_obj.error("error while scrapping %s", vehiclein)

    def get_data(self, vehiclein):
        """
        This function will take data by vehiclein id
        """
        # import pdb;pdb.set_trace()
        # sleep(1)
        open_recalls = self.get_status_info(vehiclein)

        if open_recalls.value:

            recals_data = self.jdata['nhtsa']
            if len(recals_data) == 0:
                if self.jdata['recalls']:
                    recals_data = self.jdata['recalls']
                else:
                    self.utils.recall_csv(open_recalls=open_recalls.name,
                                        recall_status="",
                                        vim_id=vehiclein, time_stamp=datetime.datetime.now())

            for recal_info in recals_data:

                date_of_recall_announcement = recal_info.get('recallDate')
                if not date_of_recall_announcement:
                    date_of_recall_announcement = recal_info.get('launchDate', '')

                self.utils.recall_csv(open_recalls=open_recalls.name,
                                      recall_status="Incomplete",
                                      name_of_recall=recal_info.get('description', '').strip(),
                                      campaign_nhsta=recal_info.get('nhtsaRecallNumber', ''),
                                      date_of_recall_announcement=date_of_recall_announcement,
                                      brief_description=recal_info.get('recallDescription', ''),
                                      safety_risk=recal_info.get('safetyRiskDescription', ''),
                                      remedy=recal_info.get('remedyDescription', ''),
                                      vim_id=vehiclein, time_stamp=datetime.datetime.now()
                                      )

            csp_count = self.jdata.get('cspCount',0)
            if csp_count > 0:
                self.get_customer_data(self.jdata, vehiclein)
            else:
                self.utils.customer_satisfaction(vim_id=vehiclein,
                                                 time_stamp=datetime.datetime.now())
        else:
            self.utils.recall_csv(open_recalls=open_recalls.name,
                                  recall_status="",
                                  vim_id=vehiclein,
                                  time_stamp=datetime.datetime.now()
                                  )
            csp_count = self.jdata.get('cspCount',0)
            if csp_count > 0:
                self.get_customer_data(self.jdata, vehiclein)
            else:
                self.utils.customer_satisfaction(vim_id=vehiclein,
                                                 time_stamp=datetime.datetime.now())

    def get_customer_data(self, jdata, vehiclein):
        """
        This function is used to get the customer satisfaction data
        """
        customer_satisfaction = jdata.get('fsa')
        for index in customer_satisfaction:
            self.utils.customer_satisfaction(
                vim_id=vehiclein,
                csp_count=jdata.get('cspCount', ''),
                name_of_description=index.get('description', ''),
                fsa_number=index.get('fsaNumber', ''),
                time_stamp=datetime.datetime.now()
            )

    def multi_threading(self, csvfile_name):
        """
        This function is used to create multiple threads to process the data
        """
        self.vin.extend(self.utils.get_vin(csvfile_name))
        self.utils.creating_files(customer_satisfaction=True)
        # print(len(self.vin))
        with ThreadPoolExecutor() as executor:
            executor.map(self.get_data, self.vin)

if __name__ == '__main__':
    file_name = sys.argv[1]
    obj = Ford()
    obj.multi_threading(file_name)
