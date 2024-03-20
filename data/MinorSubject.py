from bs4 import BeautifulSoup
import requests
import pandas as pd
import customtkinter as ctk
import re


class Minor:
    """To get the modules names, points, semester and status for the choosen minor as a dataframe"""
    def __init__(self, url_minor):
        self.url = url_minor

        self.response = requests.get(url_minor)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

        # Assuming the table title is in an h3 element and the table is in a table element
        self.table_titles = self.soup.find_all('h1')  # Adjust the tag accordingly
        self.tables = self.soup.find_all('table')  # Adjust the tag accordingly

        # Iterate through each title and table
        for title, table in zip(self.table_titles, self.tables):
            # Extract the title text
            self.title_text = title.get_text(strip=True).replace('\n', ' ').replace('\r', ' ').replace('\t',
                                                                                                       ' ').replace(
                'Nebenfach (fw)', ' Nebenfach (fw)').replace('Kernfach (fw)', ' Kernfach (fw)')
            self.title_text = re.sub(r'\s{2,}', ' : ', self.title_text)  # Replace multiple spaces with a single space

        # Extract tables
        self.dfs = pd.read_html(self.url)

        # Get first table
        self.df = self.dfs[0]

        self.word_to_check = 'Zusätzlich'

        # Delete rows containing the word in column
        self.df = self.df[~self.df['Kürzel'].str.contains(self.word_to_check)]
        self.columns_specific = ['Bezeichnung', 'LP1', 'Empf. Beginn2', 'Bindung3']

        self.index_stop = self.df.index[self.df['uPr6'] == "Auslaufende Module"].tolist()
        if self.index_stop:
            self.df = self.df.iloc[0:self.index_stop[0]]

        self.index_stop2 = self.df.index[self.df['uPr6'] == "Eingestellte Module"].tolist()
        if self.index_stop2:
            df = self.df.iloc[0:self.index_stop2[0]]

    def title(self):
        return self.title_text

    def dfminor(self):
        return self.df[self.columns_specific]