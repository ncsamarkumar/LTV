"""Importing necessary modules"""
import os
import datetime
import pandas as pd
from constants import CSV_HEADERS, OUTPUT_FOLDER

class Myutils:
    """This class funtions will be taken by ford and chevrolet"""

    def __init__(self, name):
        self.name = name

    def get_vin(self, csv_file):
        """This function will return all the vehicle vin numbers from csv file"""

        path = f"{csv_file}"
        data_frame = pd.read_excel(path, sheet_name=self.name)
        data_frame = data_frame.iloc[0:, 0]
        return data_frame.to_list()

    def creating_files(self, customer_satisfaction=False):
        """This function will create csv files"""

        folder_exist = os.path.exists(OUTPUT_FOLDER)
        if not folder_exist:
            os.makedirs(OUTPUT_FOLDER)

        if customer_satisfaction:
            header2 = ['vim_id', 'cspCount', 'name_of_description', 'fsa_number', 'time_stamp']
            dataf = pd.DataFrame(columns=header2)
            dataf.to_csv(f'{OUTPUT_FOLDER}/{self.name}CustomerSatisfaction.csv'\
                      , index=False, encoding='utf-8-sig')

        dataf = pd.DataFrame(columns=CSV_HEADERS)
        dataf.to_csv(f'{OUTPUT_FOLDER}/{self.name}Recall.csv', index=False, encoding='utf-8-sig')

    def customer_satisfaction(self, vim_id="", csp_count="", name_of_description="", fsa_number="",
                              time_stamp=""):
        """
        Append the customer satisfacation data into csv

        :param fsa_number:
        :param name_of_description:
        :param time_stamp:
        :param vim_id:
        :param csp_count:
        :param description:
        :param campaign:s

        """
        data = {'vim_id': [vim_id], 'cspCount': [csp_count], \
                'name_of_description': [name_of_description],
                'fsa_number': [fsa_number], "time_stamp": [time_stamp]}

        dataf = pd.DataFrame(data=data)
        dataf.to_csv(f'{OUTPUT_FOLDER}/{self.name}CustomerSatisfaction.csv', \
                  mode='a', header=False, index=False, encoding='utf-8-sig')

    def recall_csv(self, open_recalls="", recall_status="", name_of_recall="",
                   campaign_nhsta="", date_of_recall_announcement="",\
                   brief_description="", safety_risk="", remedy="",
                   vim_id="", time_stamp=""):
        """
        This function will insert data into csv
        """
        data = {'Open_Recalls': [open_recalls], 'Recall_status': \
                [recall_status], 'Name_of_Recall': [name_of_recall],
                'Campaign_NHTSA': [campaign_nhsta], \
                'Date_of_recall_announcement': [date_of_recall_announcement],
                'Brief_Description': [brief_description], \
                'Safety_Risk': [safety_risk], 'Remedy': [remedy],
                'Vim_ID': [vim_id], 'Time_Stamp': [time_stamp]}

        dataf = pd.DataFrame(data=data)
        dataf.to_csv(f'{OUTPUT_FOLDER}/{self.name}Recall.csv', mode='a', \
                  header=False, index=False, encoding='utf-8-sig')
