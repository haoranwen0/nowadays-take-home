from playwright.sync_api import sync_playwright
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AutofillRFP:
    def __init__(self, venue_website, event_details):
        self.venue_website = venue_website
        self.event_details = event_details

    def get_openai_input(self, input_field):
        client = OpenAI(api_key=OPENAI_API_KEY)

        print(input_field)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"What information from the following should I use in this input field, {input_field}? Here is the information I have in a stringified JSON format: {json.dumps(self.event_details)}. Just return the value, nothing else."},
            ]
        )

        return response.choices[0].message.content

    def fill_rfp(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            # Navigate to the webpage containing the form
            page.goto(self.venue_website)

            input_elements_1 = page.query_selector_all('form input')
            input_elements_2 = page.query_selector_all('form textarea')

            input_elements = input_elements_1 + input_elements_2

            for input_element in input_elements:
                # Get the label associated with the input (if available)
                label = input_element.evaluate('(input) => input.labels[0].textContent') or 'No Label'
                # Get the input's name and value
                name = input_element.get_attribute('name')

                field_label = label or ''
                field_label += name or ''

                value = self.get_openai_input(field_label)

                print(value)

                input_element.fill(value)

            # Submit the form
            page.click('button[type="submit"]')

            # Close the browser
            browser.close()

autofill_rfp = AutofillRFP("https://www.pigandkhao.com/contact", { 'firstname': 'Haoran', 'lastname': 'Wen', 'email': 'hran.wen@gmail.com', 'subject': 'Venue Reservation Inquiry', 'message': 'Hi, I\'m looking to book this venue for 4/28/24 for 25 people. Would this be possible?' })
autofill_rfp.fill_rfp()

