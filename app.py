# app.py
import streamlit as st
import os
import pandas as pd
from buffalo_scraper import extract_BUFFALO_permits
from trempealeau_scraper import extract_TREMPEALEAU_permits
from waushara_scraper import extract_WAUSHARA_permits
from grant_scraper import extract_GRANT_permits
from marathon_scraper import extract_MARATHON_permits
from lafayette_scraper import extract_LAFAYETTE_permits
import requests

st.title("Wisconsin County Permit Viewer")

st.write("Click a county button below to scrape and view permits:")

year = st.number_input("Enter the year to search permits for:", min_value=2000, max_value=2100, value=2025, step=1)

#Buffalo button (done)

if st.button("Buffalo County"):
    with st.spinner("Scraping Buffalo County data..."):
        df = extract_BUFFALO_permits(year)
        if not df.empty:
            st.success(f"✅ {len(df)} Uniform-Dwelling-Code permits found for Buffalo County!")
                        # Build the Map Link column with real buttons
            df["Map Link"] = df.apply(
                lambda row: f"""<a href="https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}" target="_blank"><button style='background-color:#4CAF50;color:white;padding:6px 10px;border:none;border-radius:4px;cursor:pointer;'>Open Map</button></a>"""
                if pd.notnull(row["Latitude"]) and pd.notnull(row["Longitude"])
                else "",
                axis=1
)

            # Enforce desired column order (same names)
            desired_order = [
                "Owner",
                "Mailing Address",
                "Property Address",
                "Parcel Number",
                "Map Link"
            ]
            filtered_df = df[[col for col in desired_order if col in df.columns]]

            # Render as interactive HTML table
            st.markdown(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
            st.error("No data found or scraping failed.")


#Trempealeau button (done)

if st.button("Trempealeau County"):
    with st.spinner("Scraping Trempealeau County..."):
        df = extract_TREMPEALEAU_permits(year)
        if not df.empty:
            st.success(f"✅ {len(df)} sanitary permits found for Trempealeau County!")
            # Build the Map Link column with real buttons
            df["Map Link"] = df.apply(
                lambda row: f"""<a href="https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}" target="_blank"><button style='background-color:#4CAF50;color:white;padding:6px 10px;border:none;border-radius:4px;cursor:pointer;'>Open Map</button></a>"""
                if pd.notnull(row["Latitude"]) and pd.notnull(row["Longitude"])
                else "",
                axis=1
)

            # Enforce desired column order (same names)
            desired_order = [
                "Owner",
                "Mailing Address",
                "Property Address",
                "Parcel Number",
                "Map Link"
            ]
            filtered_df = df[[col for col in desired_order if col in df.columns]]

            # Render as interactive HTML table
            st.markdown(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
            st.error("No data found or scraping failed.")


#Waushara button (done)

if st.button("Waushara County"):
    with st.spinner("Scraping Waushara County..."):
        df = extract_WAUSHARA_permits(year)
        if not df.empty:
            st.success(f"✅ {len(df)} sanitary permits found for Waushara County!")
             # Build the Map Link column with real buttons
            df["Map Link"] = df.apply(
                lambda row: f"""<a href="https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}" target="_blank"><button style='background-color:#4CAF50;color:white;padding:6px 10px;border:none;border-radius:4px;cursor:pointer;'>Open Map</button></a>"""
                if pd.notnull(row["Latitude"]) and pd.notnull(row["Longitude"])
                else "",
                axis=1
)

            # Enforce desired column order (same names)
            desired_order = [
                "Owner",
                "Mailing Address",
                "Property Address",
                "Parcel Number",
                "Map Link"
            ]
            filtered_df = df[[col for col in desired_order if col in df.columns]]

            # Render as interactive HTML table
            st.markdown(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
            st.error("No data found or scraping failed.")


#Grant button (done)
if st.button("Grant County"):
    with st.spinner("Scraping Grant County..."):
        df = extract_GRANT_permits(year)
        if not df.empty:
            st.success(f"✅ {len(df)} sanitary permits found for Grant County!")

            # Build the Map Link column with real buttons
            df["Map Link"] = df.apply(
                lambda row: f"""<a href="https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}" target="_blank"><button style='background-color:#4CAF50;color:white;padding:6px 10px;border:none;border-radius:4px;cursor:pointer;'>Open Map</button></a>"""
                if pd.notnull(row["Latitude"]) and pd.notnull(row["Longitude"])
                else "",
                axis=1
)

            # Enforce desired column order (same names)
            desired_order = [
                "Owner",
                "Mailing Address",
                "Property Address",
                "Parcel Number",
                "Map Link"
            ]
            filtered_df = df[[col for col in desired_order if col in df.columns]]

            # Render as interactive HTML table
            st.markdown(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
            st.error("No data found or scraping failed.")


#Marathon button (done)

if st.button("Marathon County"):
    with st.spinner("Scraping Marathon County..."):
        df = extract_MARATHON_permits(year)
        if not df.empty:
            st.success(f"✅ {len(df)} Single-Family-Home permits found for Marathon County!")
            # Add Map Link buttons directly in Streamlit
            df["Map Link"] = df.apply(
                lambda row: f"""<a href="https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}" target="_blank"><button style='background-color:#4CAF50;color:white;padding:6px 10px;border:none;border-radius:4px;cursor:pointer;'>Open Map</button></a>"""
                if pd.notnull(row["Latitude"]) and pd.notnull(row["Longitude"])
                else "",
                axis=1
            )

            # Order: Owner, Mailing Address, Site Address, Parcel Number, Map Link
            desired_order = [
                "Owner",
                "Mailing Address",
                "Site Address",
                "Parcel Number",
                "Map Link"
            ]
            filtered_df = df[[col for col in desired_order if col in df.columns]]

            # Render with clickable map buttons
            st.markdown(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
            st.error("No data found or scraping failed.")

#Lafayette button (done)

if st.button("Lafayette County"):
    with st.spinner("Scraping Lafayette County..."):
        df = extract_LAFAYETTE_permits(year)
        if not df.empty:
            st.success(f"✅ {len(df)} building permits found for Lafayette County!")
            # Add Map Link buttons directly in Streamlit
            df["Map Link"] = df.apply(
                lambda row: f"""<a href="https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}" target="_blank"><button style='background-color:#4CAF50;color:white;padding:6px 10px;border:none;border-radius:4px;cursor:pointer;'>Open Map</button></a>"""
                if pd.notnull(row["Latitude"]) and pd.notnull(row["Longitude"])
                else "",
                axis=1
            )

            # Order: Owner, Mailing Address, Site Address, Parcel Number, Map Link
            desired_order = [
                "Owner",
                "Mailing Address",
                "Site Address",
                "Parcel Number",
                "Map Link"
            ]
            filtered_df = df[[col for col in desired_order if col in df.columns]]

            # Render with clickable map buttons
            st.markdown(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
            st.error("No data found or scraping failed.")

#Iowa (done)

uploaded_file = st.file_uploader("Iowa County", type="xlsx", key="iowa_file")

if uploaded_file is not None and st.button("Find SF Homes"):
    with st.spinner("Processing all sheets for SF Residence parcels..."):

        try:
            excel = pd.ExcelFile(uploaded_file)
            sheet_names = excel.sheet_names
        except Exception as e:
            st.error(f"❌ Failed to open Excel file:\n{e}")
            st.stop()

        combined_rows = []

        for sheet in sheet_names:
            try:
                # Skip town name + blank row; use row 3 as headers
                df_sheet = pd.read_excel(uploaded_file, sheet_name=sheet, skiprows=2)

                # Filter rows where column 2 contains "SF"
                if df_sheet.shape[1] < 2:
                    continue  # Skip malformed sheets

                sf_rows = df_sheet[df_sheet.iloc[:, 1].astype(str).str.contains("SF", case=False, na=False)]
                combined_rows.append(sf_rows)

            except Exception as e:
                st.warning(f"⚠️ Skipping sheet '{sheet}' due to error: {e}")

        if not combined_rows:
            st.error("❌ No matching SF Residence rows found across any sheet.")
            st.stop()

        df = pd.concat(combined_rows, ignore_index=True)
        st.success(f"{len(df)} SF permits found for Iowa county")

        # Detect parcel column 8
        try:
            parcel_column = df.columns[7]
        except IndexError:
            st.error("❌ Cannot locate parcel column (8th column missing).")
            st.stop()

        # -------------------------------
        # Fetch parcel info from ArcGIS
        # -------------------------------
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

        # Loop through parcels and enrich data
        latitudes, longitudes, mailing_addresses = [], [], []

        for i, row in df.iterrows():
            parcel_id = str(row[parcel_column]).strip()
            lat, lon, mailing = get_parcel_info(parcel_id, "IOWA")
            latitudes.append(lat)
            longitudes.append(lon)
            mailing_addresses.append(mailing)
            print(f"📬 {parcel_id} -> {mailing}")

        # Add columns to DataFrame
        df["Latitude"] = latitudes
        df["Longitude"] = longitudes
        df["Mailing Address"] = mailing_addresses

        # Generate HTML button for each map link
        df["Map Link"] = df.apply(
            lambda row: f"""<a href="https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}" target="_blank"><button style='background-color:#4CAF50;color:white;padding:6px 10px;border:none;border-radius:4px;cursor:pointer;'>Open Map</button></a>"""
            if pd.notnull(row["Latitude"]) and pd.notnull(row["Longitude"])
            else "",
            axis=1
        )

        # ✅ Choose and order only desired columns
        desired_columns = ["Name", "Mailing Address", "Address", parcel_column, "Date", "Map Link"]
        filtered_df = df[[col for col in desired_columns if col in df.columns]]

        # ✅ Display with clickable buttons
        st.markdown(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)
