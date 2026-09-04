import pandas as pd
from bs4 import BeautifulSoup
import random as rnd
import requests
from download_manager import download_manager
from datetime import datetime, timedelta
import urllib3
urllib3.disable_warnings()




DATA_FOLDER = 'data_to_parse'
SPREADSHEET_ID = '1t4pHmphNxf7V68vrgbQbM14qGh_kQvnSIuwsb2em3KE'
GID = '1628639957'
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv#gid={GID}"
FILE_NAME = 'seed_organizations'



class company_chooser(object):
    def __init__(self, url, file_name ):
        self.url = url
        self.file_name = file_name

    def get_data_from_gsheets(self):
        '''
        Get data from google sheets and save as csv file
        :return:
        '''
        dm = download_manager()
        dm.download_file(self.url,
                         self.file_name)



    def csv_reader(self):
        # read csv and get random companies from
        df_companies = pd.read_csv(f'{DATA_FOLDER}/seed_organizations.csv', header=0)
        return df_companies




    def get_rand_companies_and_save(self):
        df = self.csv_reader()

        sample = df.sample(n=12, replace=False)

        out_path = f'{DATA_FOLDER}/random_companies.csv'
        sample.to_csv(out_path, index=False)





    def get_additional_data(self):
        # get from site Founding year, HQ country, One-sentence description
        # url where got data from
        # retrieved_at when was parsed
        df = pd.read_csv(f'{DATA_FOLDER}/random_companies.csv', header=0)

        descriptions = []
        retrived_at = []

        for domain in df['domain']:
            url = domain if domain.startswith('http') else f'https://{domain}'
            try:
                r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "html.parser")

                desc = soup.find("meta", attrs={"name": "description"})
                og_desc = soup.find("meta", attrs={"property": "og:description"})
                # h1 from html
                h1 = soup.find("h1")
                desc_from_html = h1.get_text(strip=True) if h1 else None

                value_desc = (desc or og_desc or desc_from_html)["content"] if (desc or og_desc or desc_from_html) else None

            except Exception as e:
                print(url, "-> error:", e)
                value_desc = e

            descriptions.append(value_desc)
            retrived_at.append(datetime.now())

        df['description'] = descriptions
        df['retrived_at'] = retrived_at

        df.to_csv(f'{DATA_FOLDER}/random_companies.csv', index=False)



if __name__ == '__main__':
    companies = company_chooser(GSHEET_URL, FILE_NAME)
    companies.get_data_from_gsheets()

    # get rand companies to parse
    companies.get_rand_companies_and_save()
    companies.get_additional_data()



