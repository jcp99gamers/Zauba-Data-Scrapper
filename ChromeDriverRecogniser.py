import os
import re
import sys
import shutil
import winreg
import zipfile
import requests
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

def get_version_difference(version1, version2):
    """
    This function takes in two version numbers as strings and returns the absolute difference between them.
    """
    version1_components = version1.split('.')
    version2_components = version2.split('.')
    difference = 0
    for i in range(len(version1_components)):
        difference += abs(int(version1_components[i]) - int(version2_components[i]))
    return difference
def find_closest_number_index(numbers_list, target_number):
    """
    This function takes in a list of version numbers and a target version number, and returns the index
    of the version number in the list that is closest to the target version number.
    """
    closest_index = 0
    closest_difference = get_version_difference(numbers_list[0], target_number)
    for i in range(1, len(numbers_list)):
        current_difference = get_version_difference(numbers_list[i], target_number)
        if current_difference < closest_difference:
            closest_index = i
            closest_difference = current_difference
    return closest_index

url = "https://chromedriver.chromium.org/downloads"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

versions = []
for span in soup.find_all("span", {"class": ["C9DxTc aw5Odc", "C9DxTc"]}):
    version = span.get_text().strip()
    if version.startswith("ChromeDriver "):
        versions.append(version.replace("ChromeDriver ", ""))


version_numbers = []
# regex pattern for version numbers in format major.minor.patch
version_pattern = r'\d+\.\d+\.\d+\.\d\d'

# iterate over each item in the list
for item in versions:
    # find all version numbers in the item
    matches = re.findall(version_pattern, item)
    # add all version numbers found to the list of version numbers
    version_numbers.extend(matches)

available_version_numbers = list(set(version_numbers))#sorted(, reverse=True)
# available_version_numbers.sort(reverse=True)
# print("Available ChromeDriver Versions:",available_version_numbers)


def get_chrome_version():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
        value, regtype = winreg.QueryValueEx(key, 'version')
        return value
    except WindowsError:
        return None

chrome_version = get_chrome_version()
if chrome_version:
    # print("Chrome version: " + chrome_version)
    pass
else:
    print("Chrome is not installed on this system.")
    sys.exit(0)

closest_index = find_closest_number_index(available_version_numbers, chrome_version)
closest_version_number = available_version_numbers[closest_index]
# print(closest_version_number)

# Set the URL to download the Chrome Driver
url = r'https://chromedriver.storage.googleapis.com/'+closest_version_number+r'/chromedriver_win32.zip'

# # Set the path to save the downloaded file
# download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.zip')

# # Download the file from the specified URL
# urllib.request.urlretrieve(url, download_path)

# # Unzip the downloaded file to the same folder
# with zipfile.ZipFile(download_path, 'r') as zip_ref:
#     zip_ref.extractall(os.path.dirname(download_path))

# # Delete the downloaded zip file
# os.remove(download_path)


# Set the path to save the downloaded file
download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.zip')
# Delete the downloaded zip file if it exists
if os.path.exists(download_path):
    os.remove(download_path)

# Download the file from the specified URL
urllib.request.urlretrieve(url, download_path)

# Extract the downloaded file to the "Child Drivers" folder
extract_path = Path(os.path.dirname(os.path.abspath(__file__))) / "Drivers"
# Delete the path if Exists
if os.path.exists(extract_path):
    shutil.rmtree(extract_path)

with zipfile.ZipFile(download_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Delete the downloaded zip file
os.remove(download_path)