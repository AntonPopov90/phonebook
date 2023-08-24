import re
import pandas as pd
import phonenumbers  # library for check mobile phonenumbers
import fire  # library for simple work on console


class Phonebook:
    """Class for CRUD operation with phonebook.txt file. For work in console there are 4 coomands:
    Write in console:

    1. python main.py show_by_pages - shows all phonebook by pages


    2. python main.py add_new_record - adds new record(don't forget quotes).
    Example:
    python main.py add_new_record 'иванов иван иванович МЧС +7999999999 911'


    3. python main.py edit_record - find required string and change by surname and name it was finded.
    python main.py edit_record 'surname' 'name' 'new data'
    Example:
     python main.py edit_record 'Иванов' 'Иван' 'Гаврилов Гаврила Гаврилович Параллакс +788888888 56789'


    4. python main.py find_record - try to find required record.
     python main.py find_record 'search columns' 'search words'

    Example:
      python main.py find_record 'имя организация фамилия' 'иван мчс иванов'


    """

    phonebook = pd.read_csv('phonebook.txt', sep=' ')
    headlines = ['фамилия', 'имя', 'отчество', 'организация', 'номер(сот.)', 'номер(раб.)']

    @staticmethod
    def check_input_values(value: str) -> dict or None:
        """validation of input data"""
        result_record = value.split(sep=' ')  # convert input string to list

        #  check amount of input data
        if len(result_record) < 6:
            print(f"You forget something, please check information in quotes\n"
                  f"You give {len(result_record)} objects,but must be 6\n"
                  "Example command: python main.py add_new_record 'иванов иван иванович  МЧС +7999999999 911'")
            return None
        elif len(result_record) > 6:
            print("You wrote to much information. Please check information in quotes\n"
                  "or, maybe there are additional space behind words\n"
                  "Example command: python main.py add_new_record 'иванов иван иванович  МЧС +7999999999 911'")
            return None

        #  checking for symbols and numbers in full name
        for i in range(0, 3):
            if result_record[i].isalnum():
                if re.search('\d', result_record[i]):
                    print("You make mistake in: {result_record[i]}. Full name must contain only letters")
                    return None
            else:
                print(f"You make mistake in: {result_record[i]}. Full name must contain only letters")
                return None

        # checks correct mobile phone number
        try:
            phonenumbers.parse(result_record[4])
        except phonenumbers.phonenumberutil.NumberParseException:
            print("Not correct mobile phone number. Try to write number with '+' before digits")
            return None
        try:
            data = {'фамилия': str(result_record[0]).lower(),  # prepare data for writing
                    'имя': str(result_record[1]).lower(),
                    'отчество': str(result_record[2]).lower(),
                    'организация': str(result_record[3]).lower(),
                    'телефон(сот.)': str(result_record[4]).lower(),
                    'телефон(раб.)': str(result_record[5]).lower()}
            return data
        except ValueError:
            print('Something wrong with input data\n'
                  'Available only letters in full name and organization\n'
                  'and only digits in phonenumbers')

    def show_by_pages(self) -> print:
        """show phonebook by pages"""
        phonebook = pd.read_csv('phonebook.txt', sep=' ', skip_blank_lines=True)
        print(phonebook)


    def add_new_record(self, record: str) -> str:
        """add new record to phonebook.txt."""

        data = self.check_input_values(record)

        if data is not None:
            df = pd.DataFrame([data])  # create pandas DataFrame
            df.to_csv('phonebook.txt', mode='a', header=False, index=False, sep=' ')  # write data to phonebook.txt
            return 'Record successfully added to phonebook.'

    def edit_record(self, surname: str, name: str, new_record: str) -> str:
        """FInd record and overwrite it"""
        x = self.phonebook.loc[(self.phonebook['фамилия'] == surname.lower()) & (self.phonebook['имя'] == name.lower())]
        if len(x.values) < 1:
            return "Record not found"
        else:
            new_values = list(self.check_input_values(new_record).values())  # validate new values and convert to list
            old_values = list(x.values[0])  # convert old values to list
            new_df = self.phonebook.replace(old_values, new_values)  # overwrite values to phonebook.txt
            new_df.to_csv('phonebook.txt', sep=' ', index=False)
            return "Record successfully updated"

    def find_record(self, search_values: str, search_words: str) -> str or None:
        """Finds record in phonebook.txt file."""
        search_columns_list = search_values.split()
        if type(search_words) == int:
            search_words_list = str(search_words).split()

        else:
            search_words_list = search_words.split()

        print(search_words_list[0]=='911')

        if len(search_words_list) == len(search_columns_list):  # Check that lenght of 2 lists are the same
            search_query = self.phonebook  # Create a copy of the phonebook
            try:
                for value, word in zip(search_columns_list, search_words_list):
                    search_query = search_query.loc[search_query[value] == word]
                if len(search_query) < 1:
                    print('Records not found')
                else:
                    print(search_query)

            except KeyError:
                print('Firts params must be a name of columns:\n'
                      'фамилия имя отчество etc')
                return None
        else:
            print(f"Number of input do not match each other\n"
                  f"there are {len(search_columns_list)} words in the first line\n"
                  f"and {len(search_words)} words in the second line\n")





if __name__ == '__main__':
    fire.Fire(Phonebook)
