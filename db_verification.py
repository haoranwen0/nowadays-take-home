import os
import mailtrap as mt
from dotenv import load_dotenv
import pandas as pd
from validate_email import validate_email
import socket
from bs4 import BeautifulSoup

load_dotenv()
MAILTRAP_API_KEY = os.getenv('MAILTRAP_API_KEY')

class DBVerification:
	def __init__(self, csv_path, mailtrap_api_key):
		self.csv_data = pd.read_csv(csv_path)
		self.mailtrap_api_key = mailtrap_api_key

	def get_venue_info(self, selected_columns):
		venue_name_and_emails = self.csv_data[selected_columns]

		return venue_name_and_emails

	def send_inquiry(self):
		venue_info = self.get_venue_info(["venue_name", "email"])
		for _, row in venue_info.iterrows():
			venue_name = row['venue_name']
			email = row['email']
			if isinstance(venue_name, str) and isinstance(email, str):
				try:
					mail = mt.Mail(
						sender=mt.Address(email="hran.wen@gmail.com", name="Haoran Wen"),
						to=[mt.Address(email=email)],
						subject="Room Availability Inquiry",
						text=f"""Hi,

						I hope this email finds you well. My name is Haoran Wen, and I am reaching out on behalf of {venue_name}. We are in the process of planning a large event and are currently exploring potential venues that can accommodate our needs.

						We are impressed by {venue_name} and are interested in learning more about the rooms available for booking for our event. Could you please provide information on the following:

						Capacity: How many guests can each room accommodate? We anticipate 55-80 attendees and need a space that can comfortably accommodate everyone.

						Facilities: Could you please provide details on the facilities available in the rooms, such as audiovisual equipment, seating arrangements, and any other amenities?
						Pricing: What are the rental rates for the rooms? Are there any additional fees or charges we should be aware of?
						Catering Options: Do you offer catering services, or are there preferred vendors we should consider for our event?
						Booking Process: What is the process for booking a room at your venue? Are there any specific requirements or documents we need to provide?

						Additionally, if it's possible, we would appreciate a virtual tour of the available rooms to help us better visualize the space.
						We are looking forward to the possibility of hosting our event at {venue_name} and would appreciate any information you can provide. Please feel free to contact me at +1 (347)-543-6365 or hran.wen@gmail.com to discuss further or to schedule a site visit.

						Thank you for your time and assistance. We eagerly await your response.

						Warm regards,
						Haoran Wen
						Nowadays""",
					)

					client = mt.MailtrapClient(token=self.mailtrap_api_key)
					client.send(mail)
				except Exception as e:
					print(e)

		return True

	def get_invalid_emails(self):
		venue_info = self.get_venue_info(["email"])
		invalid_emails = []
		for _, row in venue_info.iterrows():
			email = row["email"]
			if isinstance(email, str):
				valid = validate_email(
					email_address=email,
					check_format=True,
					check_blacklist=True,
					check_dns=True,
					dns_timeout=10,
					check_smtp=True,
					smtp_timeout=10,
					smtp_helo_host=socket.gethostname(),
					smtp_from_address='hran.wen@gmail.com',
					smtp_skip_tls=False,
					smtp_tls_context=None,
					smtp_debug=False
				)
				if not valid:
					invalid_emails.append(email)

		return invalid_emails

# db_verification = DBVerification("./venues_db/tw-boston.csv", MAILTRAP_API_KEY)
# db_verification.get_invalid_emails()
# db_verification.send_inquiry()
