# trempealeau_scraper.py

import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

def extract_TREMPEALEAU_permits(year):
    
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Required for Docker
    options.add_argument("--disable-dev-shm-usage")  # Prevents shared memory issues
    options.add_argument("--disable-gpu")  # Optional but recommended
    options.add_argument("--remote-debugging-port=9222")  # Fixes DevToolsActivePort issue

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    wait = WebDriverWait(driver, 15)
    
    try:
        driver.get("https://ch.co.trempealeau.wi.us/gcswebportal/")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='I Accept']"))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Permit"))).click()
        time.sleep(2)

        Select(wait.until(EC.presence_of_element_located(
            (By.ID, "ctl00_cphMainApp_PermitSearchCriteria1_DropDownListDepartment")
        ))).select_by_visible_text("Department of Land Management")

        Select(wait.until(EC.presence_of_element_located(
            (By.ID, "ctl00_cphMainApp_PermitSearchCriteria1_DropDownListAppType")
        ))).select_by_visible_text("Sanitary Permit")

        year_input = wait.until(EC.presence_of_element_located((By.ID, "ctl00_cphMainApp_PermitSearchCriteria1_TextBoxYear")))
        year_input.clear()
        year_input.send_keys(str(year))

        wait.until(EC.element_to_be_clickable((By.ID, "ButtonPermitSearch"))).click()

    except Exception as e:
        print("❌ Form setup failed:", e)
        driver.quit()
        return pd.DataFrame()

    data = []
    try:
        while True:
            wait.until(EC.presence_of_element_located((By.ID, "ctl00_cphMainApp_GridViewPermitResults")))
            rows = driver.find_elements(By.CSS_SELECTOR, "#ctl00_cphMainApp_GridViewPermitResults tr")[1:]

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) < 8:
                    continue
                data.append({
                    "Permit Type": cells[0].text.strip(),
                    "Parcel Number": cells[4].text.strip(),
                    "Owner": cells[6].text.strip(),
                    "Property Address": cells[7].text.strip()
                })

            try:
                current_page = int(driver.find_element(By.CSS_SELECTOR, "#ctl00_cphMainApp_GridViewPermitResults tr td table tr td span").text.strip())
            except:
                break

            next_links = driver.find_elements(By.CSS_SELECTOR, "#ctl00_cphMainApp_GridViewPermitResults tr td table tr td a")
            next_page = next((link for link in next_links if link.text.strip().isdigit() and int(link.text.strip()) > current_page), None)

            if not next_page:
                break
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(1.5)

    except Exception as e:
        print("❌ Scraping failed:", e)
        driver.quit()
        return pd.DataFrame()

    driver.quit()
    df = pd.DataFrame(data)

    # Add coordinates
    def get_parcel_info(parcel_id, county_name="TREMPEALEAU"):
        url = "https://services3.arcgis.com/n6uYoouQZW75n5WI/arcgis/rest/services/Wisconsin_Statewide_Parcels/FeatureServer/0/query"
        params = {
            "where": f"PARCELID='{parcel_id}' AND CONAME='{county_name}'",
            "outFields": "LATITUDE,LONGITUDE,PSTLADRESS",
            "returnGeometry": "false",
            "f": "json"
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            attrs = resp.json()["features"][0]["attributes"]
            return attrs.get("LATITUDE"), attrs.get("LONGITUDE"), attrs.get("PSTLADRESS", "")
        except:
            return None, None, None

    df["Latitude"], df["Longitude"], df["Mailing Address"] = zip(*df["Parcel Number"].map(get_parcel_info))

    # NO Excel-style HYPERLINK formula here anymore
    # Just return the DataFrame
    return df