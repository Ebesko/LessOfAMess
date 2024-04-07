from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from pathlib import Path


class Minor:
    """To get the modules names, points, semester and status for the choosen minors_data as a dataframe"""

    def __init__(self, url_minor, title=""):
        self.url = url_minor
        self.title_text = title
        self.columns_specific = ['Bezeichnung', 'LP1', 'Empf. Beginn2', 'Bindung3']

        # self.filename = "../minors_data/" + self.url[50:58] + ".csv"
        self.filename = Path("./minors_data/" + self.url[50:58] + "_" + self.title_text + ".csv")
        self.filename1 = Path("./data/minors_data/" + self.url[50:58] + "_" + self.title_text + ".csv")

        if Path("./minors_data/").exists():
            self.filename = "./minors_data/" + self.url[50:58] + "_" + self.title_text + ".csv"

        if Path("./data/minors_data/").exists():
            self.filename = "./data/minors_data/" + self.url[50:58] + "_" + self.title_text + ".csv"

        try:
            self.df = pd.read_csv(self.filename)
        except:
            print("No file found, creating one...")
            self.force_minor_update()

    def force_minor_update(self):
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

        # Assuming the table title is in an h1 element and the table is in a table element
        self.table_titles = self.soup.find_all('h1')
        self.tables = self.soup.find_all('table')

        # Iterate through each title and table
        for title, table in zip(self.table_titles, self.tables):
            self.title_text = title.get_text(strip=True).replace('\n', ' ').replace('\r', ' ').replace('\t',
                                                                                                           ' ').replace(
                    'Nebenfach (fw)', ' Nebenfach (fw)').replace('Kernfach (fw)', ' Kernfach (fw)')
            self.title_text = re.sub(r'\s{2,}', ' : ',
                                         self.title_text)  # Replace multiple spaces with a single space

        # Extract tables
        self.dfs = pd.read_html(self.url)

        # Get first table
        self.df = self.dfs[0]

        # This word start a long sentence remembering the existance of 'Individuelles Ergänzungsbereich'
        # that must be removed
        self.word_to_check = 'Zusätzlich'

        # Delete rows containing the word in column
        self.df = self.df[~self.df['Kürzel'].str.contains(self.word_to_check)]

        self.index_stop = self.df.index[self.df['uPr6'] == "Auslaufende Module"].tolist()
        if self.index_stop:
            self.df = self.df.iloc[0:self.index_stop[0]]

        self.index_stop2 = self.df.index[self.df['uPr6'] == "Eingestellte Module"].tolist()
        if self.index_stop2:
            self.df = self.df.iloc[0:self.index_stop2[0]]

        self.out_minor = self.df[self.columns_specific]

        self.updatecsvminor()

    def title(self):
        return self.title_text

    def dfminor(self):
        return self.df[self.columns_specific]

    def updatecsvminor(self):
        self.out_minor.to_csv(self.filename, index=False)
