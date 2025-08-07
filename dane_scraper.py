# automate_dane_parcel.py
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from address_parser import parse_address

def automate_dane_address_search(file, column_name):
    df = pd.read_excel(file)

    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)

    try:
        for _, row in df.iterrows():
            raw_address = str(row[column_name])
            parsed = parse_address(raw_address)

            driver.get("https://accessdane.danecounty.gov/Parcel")
            time.sleep(2)

            try:
                driver.find_element(By.LINK_TEXT, "Parcel Address").click()
                time.sleep(1)

                driver.find_element(By.ID, "txtHouseNum").clear()
                driver.find_element(By.ID, "txtHouseNum").send_keys(parsed['house_number'])

                if parsed['prefix']:
                    Select(driver.find_element(By.ID, "ddlPrefixDirection")).select_by_visible_text(parsed['prefix'])

                driver.find_element(By.ID, "txtStreetName").clear()
                driver.find_element(By.ID, "txtStreetName").send_keys(parsed['street_name'])

                if parsed['street_type']:
                    Select(driver.find_element(By.ID, "ddlStreetType")).select_by_visible_text(parsed['street_type'])

                if parsed['municipality']:
                    Select(driver.find_element(By.ID, "ddlMunicipality")).select_by_visible_text(parsed['municipality'])

                driver.find_element(By.ID, "btnAddressSearch").click()
                print(f"Searched for: {raw_address}")
                time.sleep(3)

            except Exception as e:
                print(f"Error with '{raw_address}': {e}")
                continue

    finally:
        driver.quit()
