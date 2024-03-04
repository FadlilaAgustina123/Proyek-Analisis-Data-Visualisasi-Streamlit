import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt

# Read data from CSV file
all_df = pd.read_csv("all_df.csv")

# Convert 'date' column to datetime
all_df['date'] = pd.to_datetime(all_df['date'])

st.set_page_config(
    page_title="Analysis Dashboard - Bike Sharing",
    page_icon="🚴‍♂️",
    layout="wide"
)

def generate_monthly_summary(all_df):
    monthly_summary_df = all_df.resample(rule='M', on='date').agg({
        "count_x": "sum",
        "registered_x": "sum",
        "unregistered_x": "sum"
    })
    monthly_summary_df.index = monthly_summary_df.index.strftime('%b-%y')
    monthly_summary_df = monthly_summary_df.reset_index()
    monthly_summary_df.rename(columns={
        "date": "yearmonth",
        "count_x": "count",
        "unregistered_x": "unregistered",
        "registered_x": "registered"
    }, inplace=True)
    
    return monthly_summary_df

def generate_seasonal_summary(all_df):
    seasonal_summary_df = all_df.groupby("season_x").agg({
        "unregistered_x": "sum",
        "registered_x": "sum",
        "count_x": "sum"
    })
    seasonal_summary_df = seasonal_summary_df.reset_index()
    seasonal_summary_df.rename(columns={
        "count_x": "count",
        "unregistered_x": "unregistered",
        "registered_x": "registered"
    }, inplace=True)

    # Sesuaikan dengan kolom yang sesuai pada DataFrame
    seasonal_summary_df = pd.melt(seasonal_summary_df,
                                  id_vars=['season_x'],
                                  value_vars=['unregistered', 'registered'],
                                  var_name='ride_type',
                                  value_name='count_of_rides')

    seasonal_summary_df['season_x'] = pd.Categorical(seasonal_summary_df['season_x'],
                                                      categories=['Spring', 'Summer', 'Fall', 'Winter'])

    seasonal_summary_df = seasonal_summary_df.sort_values('season_x')

    return seasonal_summary_df

def generate_weekday_summary(all_df):
    weekday_summary_df = all_df.groupby("weekday_x").agg({
        "unregistered_x": "sum",
        "registered_x": "sum",
        "count_x": "sum"
    })
    weekday_summary_df = weekday_summary_df.reset_index()
    weekday_summary_df.rename(columns={
        "count_x": "total",
        "unregistered_x": "unregistered",
        "registered_x": "registered"
    }, inplace=True)
    
    weekday_summary_df = pd.melt(weekday_summary_df,
                                id_vars=['weekday_x'],
                                value_vars=['unregistered', 'registered'],  # Sesuaikan dengan kolom yang sesuai
                                var_name='ride_type',
                                value_name='count_of_rides')
    
    weekday_summary_df['weekday_x'] = pd.Categorical(weekday_summary_df['weekday_x'],
                                                   categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    weekday_summary_df = weekday_summary_df.sort_values('weekday_x')
    
    return weekday_summary_df

def generate_hourly_summary(all_df):
    hourly_summary_df = all_df.groupby("hour").agg({
        "unregistered_x": "sum",
        "registered_x": "sum",
        "count_x": "sum"
    })
    hourly_summary_df = hourly_summary_df.reset_index()
    hourly_summary_df.rename(columns={
        "count_x": "count",
        "unregistered_x": "unregistered",
        "registered_x": "registered"
    }, inplace=True)
    
    return hourly_summary_df

# Create date filter components
earliest_date = all_df["date"].min()
latest_date = all_df["date"].max()

# ----- SIDEBAR -----
with st.sidebar:
    # Add company logo
    st.image("logo.jpg")

    st.markdown("<h1 style='text-align: center;'>Filter Tanggal</h1>", unsafe_allow_html=True)

    # Ambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Pilih Rentang Tanggal:",
        min_value=earliest_date,
        max_value=latest_date,
        value=[earliest_date, latest_date]
    )

st.sidebar.markdown("<h1 style='text-align: center; font-size:25px;'>Stay connected and reach out to me</h1>", unsafe_allow_html=True)

column1, column2, column3 = st.sidebar.columns([1, 1, 1])

with column1:
    st.markdown("[![Instagram](https://skillicons.dev/icons?i=instagram)](https://www.instagram.com/fadlilaa_/)")
with column2:
    st.markdown("[![LinkedIn](https://skillicons.dev/icons?i=linkedin)](https://www.linkedin.com/in/fadlilaa/)")
with column3:
    st.markdown("[![Github](https://skillicons.dev/icons?i=github)](https://github.com/FadlilaAgustina123/)")

# Filter the main DataFrame based on date range
filtered_main_df = all_df[
    (all_df["date"] >= str(start_date)) &
    (all_df["date"] <= str(end_date))
]

# Display the filtered DataFrame
st.dataframe(filtered_main_df)

# Assign main_df to helper functions previously created
monthly_users_df_filtered = generate_monthly_summary(filtered_main_df)
weekday_users_df_filtered = generate_weekday_summary(filtered_main_df)
seasonal_users_df_filtered = generate_seasonal_summary(filtered_main_df)
hourly_users_df_filtered = generate_hourly_summary(filtered_main_df)

# ----- DASHBOARD MAIN PAGE -----
st.title(":chart_with_upwards_trend: Dicoding Bike-Sharing Analytics")
st.markdown("##")

column1, column2, column3 = st.columns(3)

with column1:
    total_rides = filtered_main_df['count_x'].sum()
    st.metric("Total Rides", value=total_rides)
with column2:
    total_unregistered_users = filtered_main_df['unregistered_x'].sum()
    st.metric("Total Unregistered Users", value=total_unregistered_users)
with column3:
    total_registered_users = filtered_main_df['registered_x'].sum()
    st.metric("Total Registered Users", value=total_registered_users)

st.markdown("---")

# ----- CHART -----

# Tren Pengguna Sepeda
fig, ax = plt.subplots(figsize=(25, 15))

# Menggunakan Altair untuk visualisasi yang berbeda
source = monthly_users_df_filtered  

# Total Users
ax.plot(source['yearmonth'], source['count'], label='Total Users', marker='o')
# Unregistered Users
ax.plot(source['yearmonth'], source['unregistered'], label='Unregistered Users', marker='o')
# Registered Users
ax.plot(source['yearmonth'], source['registered'], label='Registered Users', marker='o')

ax.set(title="Tren Pengguna Sepeda", xlabel='Bulan-Tahun', ylabel='Total User')
ax.legend()

# Menampilkan plot
st.pyplot(fig)

# Visualization in the first column
st.header("Visualizations")

st.markdown("<div style='font-size: 24px;'>Bagaimana tren peminjaman sepeda berubah berdasarkan musim (springer, summer, fall, winter) selama dua tahun (2011 dan 2012)?</div>", unsafe_allow_html=True)
with st.expander("Lihat Visualisasi"):
        custom_color_list = ['#e91e63', '#bdbdbd', '#bdbdbd', '#bdbdbd']  # Warna pink dan abu
        custom_seasonal_trend = all_df.groupby(['year_x', 'season_x'])['count_x'].sum().reset_index()

        fig, ax = plt.subplots()
        sns.barplot(data=custom_seasonal_trend, x='season_x', y='count_x', hue='year_x', palette=custom_color_list, ax=ax)
        plt.title("Tren Peminjaman Sepeda Berdasarkan Musim pada Tahun (2011 dan 2012)")
        plt.xlabel('Musim')
        plt.ylabel('Total Peminjaman')
        st.pyplot(fig)
        st.write("Dari visualisasi di atas, terlihat bahwa musim favorit pengguna sepeda adalah musim fall.")

st.markdown("<div style='font-size: 24px;'>Apakah pengguna sepeda lebih cenderung keluar saat cuaca cerah atau saat cuaca buruk?</div>", unsafe_allow_html=True)
with st.expander("Lihat Visualisasi"):
    # Mengelompokkan data berdasarkan kondisi cuaca dan menghitung total peminjaman
    weather_effect_df = all_df.groupby('weather_condition_x')['count_x'].sum().reset_index()

    # Mengganti data weather_condition dengan kondisi yang lebih deskriptif
    weather_effect_df.replace({
        'weather_condition_x': {
            1: 'Cerah',
            2: 'Kabut',
            3: 'Hujan Ringan, Salju Ringan',
            4: 'Hujan Lebat, Salju, Kabut'
        }
    }, inplace=True)

    # Mengurutkan data berdasarkan total peminjaman dengan urutan menurun
    weather_effect_df = weather_effect_df.sort_values('count_x', ascending=False)

    # Mendefinisikan palet warna
    custom_color_palette = ['#BA68C8', '#D3D3D3', '#D3D3D3', '#D3D3D3']  # Ungu dan light grey

    # Create a Streamlit app
    st.title("Perilaku Peminjaman Sepeda dalam Berbagai Kondisi Cuaca")

    # Membuat barplot dengan tampilan jumlah peminjaman di Streamlit
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x='count_x',
        y='weather_condition_x',  # Sesuaikan dengan nama kolom yang benar
        data=weather_effect_df,
        palette=custom_color_palette,
        ax=ax
    )
    plt.title("Perilaku Peminjaman Sepeda dalam Berbagai Kondisi Cuaca", loc="center", fontsize=15)
    plt.ylabel("Kondisi Cuaca")
    plt.xlabel("Total Peminjaman")

    # Menambahkan data label
    for p in ax.patches:
        width = p.get_width()
        st.markdown(f"<div style='color: black; text-align: left; margin-top: {p.get_y() + p.get_height() / 2}px; position: absolute;'>{width:,.0f}</div>", unsafe_allow_html=True)


    st.pyplot(fig)

    st.write("Dari visualisasi di atas, terlihat bahwa pengguna sepeda lebih cenderung keluar saat cuaca cerah.")

st.write("<div style='font-size: 24px;'>Bagaimana tren jumlah pengguna sepeda sewaan per jam pada hari kerja dan hari libur?</div>", unsafe_allow_html=True)
with st.expander("Lihat Visualisasi"):
    # Mengelompokkan data
    grouped_hour_custom = all_df.groupby(['workingday_x', 'hour'])['count_x'].mean().reset_index(name='average_counts')

    # Plotting dengan warna yang diubah
    fig, ax = plt.subplots(figsize=(12, 7))

    # Loop melalui nilai workingday yang unik
    for workingday, group in grouped_hour_custom.groupby('workingday_x'):
        ax.plot(group['hour'], group['average_counts'], label=f'Jenis Hari: {"Hari Kerja" if workingday else "Akhir Pekan"}', color=('blue' if workingday else 'yellow'))

    # Atur properti plot
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Jumlah Pengguna')
    ax.set_title('Rata-rata Jumlah Pengguna Rental Sepeda per Jam Berdasarkan Hari Kerja dan Libur')

    # Tampilkan legenda
    plt.legend(title='Jenis Hari', loc='upper right', labels=['Hari Kerja', 'Libur'])

    # Tampilkan plot
    plt.xticks(list(range(24)))  # Menambahkan label jam di sumbu x
    st.pyplot(fig)

    st.write("Dari visualisasi di atas, terlihat bahwa tren jumlah pengguna sepeda sewaan per jam pada hari kerja lebih tinggi pada jam 8 pagi dan 5 sore. Sementara itu, pada hari kerja, rata-rata jumlah pengguna terbanyak justru terjadi pada jam 1 siang.")

# Menambahkan informasi kredit
st.markdown(
    "<div style='text-align: center;'><h5 style='color: #777;'>All rights reserved. Developed by Fadlila Agustina</h5></div>",
    unsafe_allow_html=True
)