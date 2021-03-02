import streamlit as st
import pandas as pd
import pydeck as pdk

DATA_PATH = 'https://raw.githubusercontent.com/vinny380/Analyzing_Aibnb_Data_Toronto/main/listings.csv'
df = pd.read_csv(DATA_PATH)

@st.cache
def load_data():
    df.drop(df[df.price > 1500].index, axis=0, inplace=True)
    df.drop(df[df.minimum_nights > 30].index, axis=0, inplace=True)
    df.drop('neighbourhood_group', axis=1, inplace=True)
    df_clean = df[df['minimum_nights'].values < 10]
    df.drop(columns=['name', 'host_id', 'host_name', 'neighbourhood', 'last_review', 'reviews_per_month'], inplace=True)
    df.room_type = df.room_type.apply(lambda x: x.replace('/', ' or '))
    return df

# load data
df = load_data()
labels = list(df.room_type.unique())

# Sidebar
st.sidebar.header('Parameters')
amount_of_data_shown = st.sidebar.empty()  # Placeholder for later

st.sidebar.subheader('Price Range')
sliderbar = st.sidebar.slider('Select the maximum desired price:', 50, 1500, 130)
sliderbar_min = st.sidebar.slider('Select the minimum desired price:', 50, 1500, 50)
warning_message = st.sidebar.empty()

st.sidebar.subheader('Table')
checkbox = st.sidebar.checkbox('Show table')

st.sidebar.subheader('Type of Room:')
room = st.sidebar.multiselect(
    label='Select the desired type of room',
    default=labels,
    options=labels
)

df_filtered = df[(df.price <= sliderbar) & (df.room_type.isin(room)) & (df.price >= sliderbar_min)]

amount_of_data_shown.info('{} selected rooms'.format(df_filtered.shape[0]))

if checkbox:
    st.write(df_filtered)

if sliderbar_min > sliderbar:
    warning_message.info('Please select a minimum value smaller than {}'.format(sliderbar))

# MAIN
st.title("Map of AirBnB's in Toronto")
st.markdown('''
Toronto is Canada’s most populated city,
 it is located on the shores of Lake Ontario in the province of Ontario, it is home to the Toronto Raptors,
 Drake, University of Toronto, Blue Jays and many other famous entities.
''')
sub = st.markdown('ℹ️ Below you can see **{}** accommodations in Toronto: .'.format(', '.join(room))) # Subtitle text

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v10',
    initial_view_state=pdk.ViewState(
        latitude=43.6532,
        longitude=-79.3832,
        zoom=10,
        pitch=50,
    ),
    layers=[
        pdk.Layer( # A grid layer above
            'GridLayer',
            data=df_filtered,
            get_position='[longitude, latitude]',
            get_radius=680,
            pickable=True,
            extruded=True,
            cell_size=80,
            elevation_scale=100,
        ),
    ]
))