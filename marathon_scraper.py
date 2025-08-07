# marathon_scraper.py

import requests
import pandas as pd

def extract_MARATHON_permits(year):
    url = "https://ascent.co.marathon.wi.us/AscentPermitManagement/api/PermitSearchService"

    params = {
        "muniId": "undefined",
        "parcelNumber": "",
        "firstName": "",
        "lastName": "",
        "originalOwner": "",
        "additionalInfo": "SFH",
        "mailingAddress": "",
        "siteAddress": "",
        "permitNumber": "",
        "applicationNumber": "",
        "permitTypeId": 1,  # building permits
        "issueDate": f"{year}-01-01T06:00:00.000Z",
        "issueDateEnd": f"{year}-12-31T05:00:00.000Z",
        "page": 1,
        "numRecords": 200,
        "statusId": "",
        "userId": "undefined",
        "applicationDate": "undefined",
        "deleted": "false",
        "exactMatch": "false",
        "systemStatusId": 1,
        "orderBy": "Issued DESC"
    }

    response = requests.get(url, params=params)
    data = response.json()

    rows = []
    for permit in data.get("Results", []):
        parcel = permit.get("ParcelNum")
        address = permit.get("SiteAddress")
        issued = permit.get("Issued")
        owner = permit.get("Owners")
        if parcel:
            rows.append({
                "Parcel Number": parcel,
                "Site Address": address,
                "Issued Date": issued,
                "Owner": owner
            })

    df = pd.DataFrame(rows)

    def get_parcel_info(parcel_id, county_name="MARATHON"):
        url = (
            "https://services3.arcgis.com/n6uYoouQZW75n5WI/"
            "arcgis/rest/services/Wisconsin_Statewide_Parcels/"
            "FeatureServer/0/query"
        )
        params = {
            "where": f"PARCELID='{parcel_id}' AND CONAME='{county_name}'",
            "outFields": "LATITUDE,LONGITUDE,PSTLADRESS",
            "returnGeometry": "false",
            "f": "json"
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            features = data.get("features", [])
            if not features:
                return None, None, None
            attrs = features[0]["attributes"]
            return attrs.get("LATITUDE"), attrs.get("LONGITUDE"), attrs.get("PSTLADRESS", "").strip()
        except Exception as e:
            print(f"⚠️ Error fetching info for {parcel_id}: {e}")
            return None, None, None

    latitudes, longitudes, mailing_addresses = [], [], []

    for parcel_id_raw in df["Parcel Number"]:
        parcel_id_cleaned = parcel_id_raw.replace("-", "").strip()
        lat, lon, mailing = get_parcel_info(parcel_id_cleaned, "MARATHON")
        latitudes.append(lat)
        longitudes.append(lon)
        mailing_addresses.append(mailing)

    df["Latitude"] = latitudes
    df["Longitude"] = longitudes
    df["Mailing Address"] = mailing_addresses
    return df
