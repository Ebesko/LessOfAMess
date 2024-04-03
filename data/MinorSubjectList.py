from bs4 import BeautifulSoup
import re
import requests
import ast

url_possible_minors = "https://ekvv.uni-bielefeld.de/sinfo/publ/variante/80471673"


class Minor:
    """To get the modules names, points, semester and status for the choosen small minors_data as a dataframe"""
    def __init__(self, url_minor):
        self.url_minor = url_minor
        self.dict_nbf_link = {}
        self.dict_nbf_link2 = {}

    def connect(self):
        self.response = requests.get(self.url_minor)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

        # Find the div with class 'kombinierbare_faecher'
        self.kombinierbare_faecher_div_list = self.soup.find_all('div', class_='kombinierbare_faecher')


    def minors(self):
        try:
            self.minor_file = open("possible_minors.txt", "r")
            self.content = self.minor_file.read()
            self.minor_file.close()
            if ast.literal_eval(self.content) is not None:
                self.dict_minors = ast.literal_eval(self.content)
                return self.dict_minors
            else:
                self.force_update_minors()
                self.minors()
        except:
            self.force_update_minors()
            self.minors()

    def mini_minors(self):
        try:
            self.mini_minor_file = open("possible_mini_minors.txt", "r")
            self.mini_content = self.mini_minor_file.read()
            self.mini_minor_file.close()
            if ast.literal_eval(self.mini_content) is not None:
                self.dict_mini_minors = ast.literal_eval(self.mini_content)
                return self.dict_mini_minors
            else:
                self.force_update_mini_minors()
                self.mini_minors()

        except:
            self.force_update_mini_minors()
            self.mini_minors()

    def force_update_minors(self):
        self.connect()
        self.nebenfaecher = self.kombinierbare_faecher_div_list[0]
        self.choice_minor_dict = self.listed_minors(self.nebenfaecher, self.dict_nbf_link)

        self.dict_to_file = open("possible_minors.txt", "w")
        self.dict_to_file.write(str(self.choice_minor_dict))
        self.dict_to_file.close()

        #return self.choice_minor_dict

    def force_update_mini_minors(self):
        self.connect()
        self.kleinesnebenfaecher = self.kombinierbare_faecher_div_list[1]
        self.choice_minor_dict = self.listed_minors(self.kleinesnebenfaecher, self.dict_nbf_link2)

        self.dict_mini_to_file = open("possible_mini_minors.txt", "w")
        self.dict_mini_to_file.write(str(self.choice_minor_dict))
        self.dict_mini_to_file.close()

        #return self.choice_minor_dict

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



#available_minors = Minor(url_possible_minors)
#print(available_minors.mini_minors())
