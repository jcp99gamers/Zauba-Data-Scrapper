import FullChecker
import os
import re
import requests
import numpy as np
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Extract the downloaded file to the "Child Drivers" folder
extract_path = Path(os.path.dirname(os.path.abspath(__file__))) / "Drivers"
# Specify the path to the Chrome web driver executable
webdriver_service = Service(str(extract_path)+r"\chromedriver.exe")
# print(str(extract_path)+r"\chromedriver.exe")

while True:
    port = input("Choose Import / Export = ")
    if(port=="Import" or port=="import" or port=="IMPORT"):
        port = "import"
        break
    elif(port=="Export" or port=="export" or port=="EXPORT"):
        port = "export"
        break
    else:
        print("Try Again:- ")
        continue
# port = "input"
word = input("Enter the Product Name / HS Code = ")
# numberOfPages = int(input("How Many Pages of Data Do You Want = "))
words = word.split()
word = ""
logedin_word = ""
for x in words:
    y = x+"-"
    word += y
for x in words:
    y = x+"+"
    logedin_word += y
logedin_word = logedin_word[:-1]

filename = "{}_{}hs_code.csv".format(port,word)

url = r"https://www.zauba.com/{}-{}hs-code.html".format(port,word)# a = r"https://www.zauba.com/"+port+r"-"+word+r"hs-code.html"
print(url)

response = requests.get(url) # Make a request to the website
# Parse HTML and extract the table
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'class': 'result-table'})

# Extract the data from the table and store it in a Pandas dataframe
data = []
rows = table.find_all('tr')
html_headers = rows[0].find_all('th')
headers = []
for h in html_headers:
    head = str(h).replace('<th scope="col">', "").replace("</th>", "").strip()
    headers.append(head)
for row in rows:
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    data.append(cols)
data[0] = headers
# print(data)
df = pd.DataFrame(data[1:], columns=data[0])
df = df.dropna()

# # Create CSV
# df.to_csv("{}_{}hs_code.csv".format(port,word), index=False)
# print(df)


# Set up Selenium to use Chrome browser
chrome_options = Options()
chrome_options.add_argument('--headless')  # Use headless mode to avoid opening a visible browser window
# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
# driver = webdriver.Chrome(service=webdriver_service)
# Navigate to the login page
driver.get(url)
url = r"https://www.zauba.com/{}-{}/p-{}-hs-code.html".format(port,logedin_word,2)
string = r'</a></li><li class="pager-next"><a href="'+url+r'">'
# Get the HTML code of the page
html = driver.page_source
# Store the HTML code in a file called manuplation.html
with open('pageCounter.html', 'w', encoding="utf-8") as f:
    f.write(html)
# Open the file in read mode
with open('pageCounter.html', 'r') as file:
    # Loop through each line and find the 31st line
    for i, line in enumerate(file):
        if i == 125:
            # Return the content of the 31st line
            line126 = line.strip()
# print(len(line126))
end_index = line126.find(string)
input_string = line126[end_index-21:end_index]
start_index = input_string.find(">")
last_page_value = input_string[start_index+1:]
numberOfPages = int(last_page_value.replace(",", ""))
print("There are",numberOfPages,"Pages with Data.")
try:
    input_number = int(input("How Many Pages of Data Do You Want to Download = "))
    if(input_number<numberOfPages):
        numberOfPages = input_number
except:
    pass

# Navigate to the login page
driver.get("https://www.zauba.com/user/login")


# Get the HTML code of the page
html = driver.page_source

# Store the HTML code in a file called manuplation.html
with open('manuplation.html', 'w', encoding="utf-8") as f:
    f.write(html)

# Open the file in read mode
with open('manuplation.html', 'r') as file:
    # Loop through each line and find the 31st line
    for i, line in enumerate(file):
        if i == 30:
            # Return the content of the 31st line
            line31 = line.strip()

# print(len(line31))
# print(line31[5462:5470])
input_string = line31[5462:5470]

# regular expression pattern to match two integers and an operator
pattern = r'(\d{1,2})\s*([+*-/])\s*(\d{1,2})'

# find the first match in the input string
match = re.search(pattern, input_string)
# extract the integer values and operator from the match
if match:
    a = int(match.group(1))
    op = match.group(2)
    b = int(match.group(3))
    print(f"a = {a}, op = {op}, b = {b}")
    if op == "+":
        val = a+b
    elif op == "-":
        val = a-b
    elif op == "*":
        val = a*b
    elif op == "/":
        val = a//b
else:
    print("No match found.")

# print(val)

# Find the username input field and enter your username
# username_input = driver.find_element_by_id("edit-name")
username_input = driver.find_element(By.ID, "edit-name") # Find the element with id "edit-name"
username_input.send_keys("username_jcp")

# Find the password input field and enter your password
# password_input = driver.find_element_by_id("edit-pass")
password_input = driver.find_element(By.ID, "edit-pass") # Find the element with id "edit-pass"
password_input.send_keys("Password123")

# Find the captcha input field and enter your captcha
# captcha_input = driver.find_element_by_id("edit-pass")
captcha_input = driver.find_element(By.ID, "edit-captcha-response") # Find the element with id "edit-pass"
captcha_input.send_keys(val)

# Submit the login form by clicking the login button
# login_button = driver.find_element_by_id("edit-submit")
login_button = driver.find_element(By.ID, "edit-submit") # Find the element with id "edit-submit"
login_button.click()

# # Wait for the dashboard page to load
# dashboard_title = "Log in | Zauba"
# driver.implicitly_wait(10) # wait for 10 seconds for the dashboard page to load
# assert dashboard_title in driver.title, "Failed to login to Zauba"

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.url_to_be("https://www.zauba.com/user/538623"))


for x in range(2,numberOfPages+1):
    try:
        url = r"https://www.zauba.com/{}-{}/p-{}-hs-code.html".format(port,logedin_word,x)
        print("\t"+url)
        # Navigate to the next page
        driver.get(url)


        # Get the page source and parse it using BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Find the table in the parsed HTML
        table = soup.find('table', {'class': 'result-table'})

        # Extract the data from the table and store it in a Pandas dataframe
        data = []
        rows = table.find_all('tr')
        html_headers = rows[0].find_all('th')
        headers = []
        for h in html_headers:
            head = str(h).replace('<th scope="col">', "").replace("</th>", "").strip()
            headers.append(head)
        for row in rows:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            data.append(cols)
        data[0] = headers
        new_df = pd.DataFrame(data[1:], columns=data[0])
        new_df = new_df.dropna()
        # new_df.to_csv("{}_{}hs_code.csv".format(port,word), index=False)
        # # Print the data frame
        # print(new_df)
        df = pd.concat([df, new_df]) # concatenate the two dataframes using pd.concat
        # df = df.append(new_df) # Append new_df to 
    except Exception as e:
        print(e)
        break
    else:
        continue


try:
    # Create CSV
    df.to_csv(filename, index=False)
except Exception as e:
    print(e)
finally:
    # Reset the index to a default integer index
    df = df.reset_index()
    print(df)

# Close the browser window
driver.quit()
