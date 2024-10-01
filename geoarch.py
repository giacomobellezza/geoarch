import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import folium
from streamlit_folium import st_folium


def plot_data():
    df = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/"
        + "1Ie9ucp2dlNpTx3s-mJv9u__MJykDy2p7ShcHZVM7Hws"
        + "/export?gid=0&format=csv",
        converters={"lat": np.float64, "lon": np.float64},
    )

    unique_types = df.type.unique()
    color_palette = sns.color_palette("bright", len(unique_types))
    color_palette = [
        "red",
        "blue",
        "green",
        "purple",
        "orange",
        "darkred",
        "lightred",
        "beige",
        "darkblue",
        "darkgreen",
        "cadetblue",
        "darkpurple",
        "white",
        "pink",
        "lightblue",
        "lightgreen",
        "gray",
        "black",
        "lightgray",
    ]
    color_map = dict(zip(unique_types, color_palette))
    df["color"] = df.type.map(color_map)

    icon_list = [
        "search",
        "home",
        "leaf",
        "cog",
        "cloud",
        "star",
        "glass",
        "music",
        "heart",
        "film",
        "flag",
        "book",
    ]
    icon_map = dict(zip(unique_types, icon_list))
    df["icon"] = df.type.map(icon_map)

    # sidebar
    with st.sidebar:
        filters = dict()
        with st.form("Params"):
            left, _, right = st.columns(3)
            with left:
                st.subheader("Params")
            with right:
                st.form_submit_button(label="Apply Filters", type="primary")

            filters["type"] = st.multiselect("Type", unique_types, default=unique_types)
        
        age = st.slider("Select year up to:", df.age.min(), df.age.max(), df.age.max(),
                        help="Select the year up to which you want to filter the data. Negative values are allowed and mean BC.")

    # main
    tab1_map, tab2_data = st.tabs(["Map", "Data"])

    with tab1_map:
        data = df[df.type.isin(filters["type"])]
        data = data[data.age <= age]
        location = data[["lat", "lon"]].mean().values.tolist()

        # center on Liberty Bell, add marker
        m = folium.Map(location=location, zoom_start=8)
        for i, row in data.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=row["name"],
                tooltip=row["type"],
                icon=folium.Icon(color=row["color"], icon=row["icon"]),
            ).add_to(m)

        # call to render Folium map in Streamlit
        st_data = st_folium(m, width=725)

    with tab2_data:
        st.write(data[["name", "type", "lat", "lon", "century"]])


if __name__ == "__main__":
    plot_data()
