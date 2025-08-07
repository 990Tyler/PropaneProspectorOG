import pandas as pd
import requests

# Load filtered CSV (the one we generated earlier)
csv_path = r"C:\Users\EmmaKomis\OneDrive - Premier Cooperative\Desktop\Summer Project\IN PROGRESS\sf_residence_filtered.csv"
df = pd.read_csv(csv_path)

# ✅ Set this to the correct index if parcel number is in column 6 (0-based index 5)
parcel_column = df.columns[5]

# 🔍 Function to fetch parcel info
def get_parcel_info(parcel_id, county_name="IOWA"):
    url = (
        "https://services3.arcgis.com/n6uYoouQZW75n5WI/"
        "arcgis/rest/services/Wisconsin_Statewide_Parcels/"
        "FeatureServer/0/query"
    )
    params = {
        "where": f"PARCELID='{parcel_id}' AND CONAME='{county_name.upper()}'",
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
        attrs = features[0].get("attributes", {})
        lat = attrs.get("LATITUDE")
        lon = attrs.get("LONGITUDE")
        mailing_address = attrs.get("PSTLADRESS", "").strip()

        return lat, lon, mailing_address

    except Exception as e:
        print(f"⚠️ Error fetching info for {parcel_id}: {e}")
        return None, None, None

# 🔁 Loop through rows and fetch parcel data
latitudes = []
longitudes = []
mailing_addresses = []

for i, row in df.iterrows():
    parcel_id = str(row[parcel_column]).strip()
    lat, lon, mailing = get_parcel_info(parcel_id, "IOWA")
    latitudes.append(lat)
    longitudes.append(lon)
    mailing_addresses.append(mailing)
    print(f"📬 {parcel_id} -> {mailing}")

# 🧩 Add columns to DataFrame
df["Latitude"] = latitudes
df["Longitude"] = longitudes
df["Mailing Address"] = mailing_addresses

# 🔗 Add Google Maps link
df["Map Link"] = df.apply(
    lambda row: f"https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}"
    if pd.notnull(row["Latitude"]) and pd.notnull(row["Longitude"])
    else "",
    axis=1
)

# 💾 Save updated CSV
output_csv = csv_path.replace(".csv", "_with_coords.csv")
df.to_csv(output_csv, index=False)
print(f"✅ Done! Updated file saved to:\n{output_csv}")
