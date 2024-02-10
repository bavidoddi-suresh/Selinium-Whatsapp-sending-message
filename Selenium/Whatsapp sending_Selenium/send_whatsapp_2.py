import undetected_chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
import config as cf
import gspread
from oauth2client.service_account import ServiceAccountCredentials

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={cf.local['userDataDir']}")
service = Service(cf.local["executable_path"])
driver = webdriver.Chrome(service=service, options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
time.sleep(10)
print("opened WhatsApp")

def get_phone_numbers_and_names(sheet_link, column_number):
    # Use the credentials.json file from Google API Console
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/home/revops/Documents/Selenium/credentials.json", scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet using the extracted sheet key
    sheet = client.open_by_url(sheet_link).sheet1

    # Get all values in the specified columns (excluding header)
    data = sheet.get_all_values()[1:]

    # Initialize lists to store phone numbers and names
    phone_numbers = []
    names = []

    # Iterate through rows and stop when an empty phone number is encountered
    for row in data:
        if not row[column_number - 1]:
            break
        phone_numbers.append(row[column_number - 1])
        names.append(row[column_number])

    return phone_numbers, names

def send_whatsapp_message(phone_number, name, message_template):
    # Form the URL with phone number and personalized message
    phone_number = "+91" + phone_number  # Assuming India's country code is +91
    personalized_message = message_template.replace("<Name>", name)

    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={personalized_message}"

    # Open the URL
    driver.get(url)
    time.sleep(60)
    send_button = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
    send_button.click()
    print(f"Message sent to {name} ({phone_number})")
    time.sleep(10)

# List of phone numbers and messages
sheet_link = "https://docs.google.com/spreadsheets/d/1VEd_vHHzwT2Jb6oLuDTfm5ej_okMOISCWXCw8LsvTu0/edit#gid=1604215351"  # Replace with your actual sheet link
column_number = 1  # Replace with the column number containing phone numbers

# Get phone numbers and names from Google Sheet
phone_numbers, names = get_phone_numbers_and_names(sheet_link, column_number)
message_template = "Hey <Name> %2C%0A%0AYou%20are%20a%20huge%20part%20of%20NxtWave%E2%80%99s%20success%20in%202023%21%20%F0%9F%8E%8A%0A%0AAnd%2C%20before%20we%20step%20into%202024%2C%20here%E2%80%99s%20a%20heartfelt%20letter%20from%20our%20CEO%2C%20Mr.%20Rahul%20Attuluri%20%E2%9D%A4%EF%B8%8F%0A%0AWish%20you%20and%20your%20family%20a%20Happy%20New%20Year.%20%F0%9F%98%80"


# Loop through the list and send personalized messages
for phone_number, name in zip(phone_numbers, names):
    print(f"Phone Number: {phone_number}, Name: {name}")
    send_whatsapp_message(phone_number, name, message_template)