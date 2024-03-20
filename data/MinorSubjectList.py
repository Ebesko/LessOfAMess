from bs4 import BeautifulSoup
import re
import requests

url_possible_minors = "https://ekvv.uni-bielefeld.de/sinfo/publ/variante/80471673"


class Minor:
    """To get the modules names, points, semester and status for the choosen small minor as a dataframe"""
    def __init__(self, url_minor):
        self.url_minor = url_minor
        self.dict_nbf_link = {}
        self.dict_nbf_link2 = {}

        self.response = requests.get(self.url_minor)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

        # Find the div with class 'kombinierbare_faecher'
        self.kombinierbare_faecher_div_list = self.soup.find_all('div', class_='kombinierbare_faecher')


    def minors(self):
        self.nebenfaecher = self.kombinierbare_faecher_div_list[0]
        return self.listed_minors(self.nebenfaecher, self.dict_nbf_link)

    def little_minors(self):
        self.kleinesnebenfaecher = self.kombinierbare_faecher_div_list[1]
        return self.listed_minors(self.kleinesnebenfaecher, self.dict_nbf_link2)

    def listed_minors(self, nbf_variable, dict):
        if nbf_variable:
            # Extract and print the text within the <span> tag if present
            span_text = nbf_variable.span.get_text().strip() if nbf_variable.span else None
            if span_text:
                #print("Type:", span_text)
                pass

            # Find all <a> tags within the div
            buttons = nbf_variable.find_all('a')

            # Extract the numbers between "variante/" and ";" using regular expressions
            for button in buttons:
                button_url = button.get('href')
                match = re.search(r'variante/(\d+);', button_url)
                if match:
                    variant_number = match.group(1)

                    # Extract the text of the <a> tag, ignoring any text within <span> tags
                    button_text = ''.join(button.find_all(string=True, recursive=False)).strip()
                    if not button_text:
                        # If the text is empty, try finding text in the child elements
                        button_text = ''.join(button.find(string=True, recursive=False)).strip()

                    # print("Variant Number:", variant_number)
                    # print("Button Text:", button_text)
                    dict[button_text] = "https://ekvv.uni-bielefeld.de/sinfo/publ/variante/" + variant_number + "?m"
            #print(dict)
            return dict

        else:
            print("No div with class 'kombinierbare_faecher' found.")



#available_minors = Minor(url_possible_minors).minors()
#print(available_minors)
