import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome('./chromedriver', options=options)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import pickle
import base64
import os

def create_message(sender, to, subject, message_text):
  """Create a message for an email.
Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):
  """Send an email message.
	Args:
	    service: Authorized Gmail API service instance.
	    user_id: User's email address. The special value "me"
	    can be used to indicate the authenticated user.
	    message: Message to be sent.
	Returns:
	    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: {}'.format(message['id']))
    return message
  except:
    print ('An error occurred')

def notification(sender, to, subject, notification):
#Sender is the sender email, to is the receiver email, subject is the email subject, and notification is the email body message. All the text is str object.
    SCOPES = 'https://mail.google.com/'
    message = create_message(sender, to, subject, notification)
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # We use login if no valid credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow =  InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    send_message(service, sender, message)

def check_availability(start_date, end_date):

  url = "https://reservations.ahlsmsworld.com/Yosemite/Plan-Your-Trip/Accommodation-Search/Results"
  driver.get(url)
  time.sleep(5)

  select_element = driver.find_element(By.ID, 'box-widget_ProductSelection')
  select_object = Select(select_element)
  select_object.select_by_value('Y')


  inputElement = driver.find_element(By.ID, "box-widget_ArrivalDate")
  inputElement.clear()
  inputElement.send_keys(start_date)
  inputElement = driver.find_element(By.ID, "box-widget_DepartureDate")
  inputElement.clear()
  inputElement.send_keys(end_date)

  time.sleep(5)
  buttons = driver.find_elements(By.NAME, "wxa-form-button-submit")
  visible = [b for b in buttons if b.is_displayed()]
  visible[0].click()
  time.sleep(15)

  try:
    driver.find_element(By.ID, "tabsSearchResults")
  except Exception as e:
    print("no available room! try again later in 5 mins")
  else:
    print("room available on " + start_date + " to " + end_date)
    # notify 
    notification('wangyixuan0720@gmail.com', 'wangyixuan0720@gmail.com', 'Notification - Available Lodge on date ' + start_date + " to " + end_date + "!!!", 'Notification - Available Lodge!')


def main():
  notification('wangyixuan0720@gmail.com', 'wangyixuan0720@gmail.com', 'test', 'test')
  while(True):
    check_availability('2025/06/26', '2025/06/28')
    time.sleep(180)

if __name__ == '__main__':
	main()
