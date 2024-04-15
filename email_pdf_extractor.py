import csv
import os
import requests
from dotenv import load_dotenv

load_dotenv()
CHATPDF_API_KEY = os.getenv('CHATPDF_API_KEY')

def upload_pdf(path_to_pdf):
    files = [
        ('file', ('file', open(path_to_pdf, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'x-api-key': CHATPDF_API_KEY
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

    if response.status_code == 200:
        print('Source ID:', response.json()['sourceId'])
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
    pass

def output_to_csv(csv_str, name):
    # Open a CSV file in write mode
    with open(f'{name}.csv', "w", newline="") as csvfile:

        # Create a CSV writer object
        writer = csv.writer(csvfile, delimiter=",")

        # Write the string to the CSV file
        for row in csv_str.split("\n"):
            writer.writerow(row.split(","))

    # Close the CSV file
    csvfile.close()

def get_quote(src_id, messages, output_csv_filename):
    headers = {
        'x-api-key': CHATPDF_API_KEY,
        'Content-Type': 'application/json',
    }

    data = {
        'sourceId': src_id,
        'messages': messages
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    result = response.json()['content']

    if response.status_code == 200:
        print('Result:', result)
        output_to_csv(result, output_csv_filename)
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)

messages = [
    {
        "role": "user",
        "content": "Return the total quote, meeting room total, sleeping room total, notes in a string CSV format (exclude commas in the entries except for using as separators. For example, don't include commas in numbers i.e. use 1400 instead of 1,400) containing 4 columns and 2 rows (i.e. 'name,age,occupation\\nJohn Doe,30,Software Engineer\\nJane Doe,25,Data Scientist'). First row is the header of each group: Total Quote, Meeting Room Total, Sleeping Room Total, and Notes. Second row is the values for total quote, meeting room total, sleeping room total, and notes. If you can't calculate a value for total quote, meeting room total, or sleeping room total, put it in the notes section and why it can't be calculated. If you can calculate a value for them, put the formula for each in the notes section. Put any other additional information in the notes section as well. ",
    }
]

class QuoteParser:
    def __init__(self, chatpdf_api_key):
        self.CHATPDF_API_KEY = chatpdf_api_key

    def upload_pdf(self, path_to_pdf):
        files = [
            ('file', ('file', open(path_to_pdf, 'rb'), 'application/octet-stream'))
        ]
        headers = {
            'x-api-key': self.CHATPDF_API_KEY
        }

        response = requests.post(
            'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

        if response.status_code == 200:
            print('Source ID:', response.json()['sourceId'])
            return response.json()['sourceId']
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)

    def output_to_csv(self, csv_str, name):
        # Open a CSV file in write mode
        with open(f'{name}.csv', "w", newline="") as csvfile:

            # Create a CSV writer object
            writer = csv.writer(csvfile, delimiter="-")

            # Write the string to the CSV file
            for row in csv_str.split("\n"):
                writer.writerow(row.split(","))

        # Close the CSV file
        csvfile.close()

    def get_quote(self, src_id, output_csv_filename):
        headers = {
            'x-api-key': CHATPDF_API_KEY,
            'Content-Type': 'application/json',
        }

        data = {
            'sourceId': src_id,
            'messages': messages
        }

        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

        result = response.json()['content']

        if response.status_code == 200:
            print('Result:', result)
            output_to_csv(result, output_csv_filename)
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)

    def run_multiple(self, pdfs):
        for pdf in pdfs:
            pdf_src_id = self.upload_pdf(f'./sample_quotes/{pdf}.pdf')
            self.get_quote(pdf_src_id, pdf)

# upload_pdf('./sample_quotes/Get Nowadays - 07-10 October 2024 Group Accommodation Proposal.pdf')
# get_quote('src_nxutNqQGnO3lZrWYdtFy3', messages, 'divan')

pdfs = ['byotell', 'divan', 'eden_roc']
quote_parser = QuoteParser(CHATPDF_API_KEY)
quote_parser.run_multiple(pdfs)

