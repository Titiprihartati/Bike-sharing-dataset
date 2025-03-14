import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')

st.write(
    """
    # Proyek Analisis Data
    by: Titi Prihartati
    """
)
bike_df = pd.read_csv("https://raw.githubusercontent.com/Titiprihartati/Bike-sharing-dataset/main/day.csv")
bike2_df = pd.read_csv("https://raw.githubusercontent.com/Titiprihartati/Bike-sharing-dataset/main/hour.csv")
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])
bike2_df['dteday'] = pd.to_datetime(bike2_df['dteday'])

with st.sidebar:

    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    min_date = bike_df['dteday'].min()
    max_date = bike_df['dteday'].max()

    start_date, end_date = st.date_input(
    label='Periode Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
    )
bike_df = bike_df[(bike_df['dteday'] >= pd.to_datetime(start_date)) &
                (bike_df['dteday'] <= pd.to_datetime(end_date))]
bike2_df = bike2_df[(bike2_df['dteday'] >= pd.to_datetime(start_date)) &
                  (bike2_df['dteday'] <= pd.to_datetime(end_date))]
# Pertanyaan ke-1
st.write("*1. Bagaimana pengaruh suhu terhadap jumlah sepeda yang disewa?*")

# Grouping berdasarkan suhu (dibagi dalam interval)
bike_df["temp_group"] = pd.qcut(bike_df["temp"], q=4, labels=["Dingin", "Sejuk", "Hangat", "Panas"])
bike2_df["temp_group2"] = pd.qcut(bike2_df["temp"], q=4, labels=["Dingin", "Sejuk", "Hangat", "Panas"])

# Analisis statistik berdasarkan suhu
temp_analysis = bike_df.groupby("temp_group").agg({
    "cnt": ["mean", "median", "min", "max", "std"],
    "registered": ["mean", "sum"],
    "casual": ["mean", "sum"]
})
temp_analysis2 = bike2_df.groupby("temp_group2").agg({
    "cnt": ["mean", "median", "min", "max", "std"],
    "registered": ["mean", "sum"],
    "casual": ["mean", "sum"]
})
# Tampilkan hasil analisis suhu
st.write(temp_analysis)
st.write(temp_analysis2)

# Hitung rata-rata penyewaan per kategori suhu
avg_rentals_per_temp = bike_df.groupby("temp_group")["cnt"].mean().reset_index()

# Visualisasi menggunakan seaborn
plt.figure(figsize=(8, 5))
sns.barplot(data=avg_rentals_per_temp, x="temp_group", y="cnt", order=["Dingin", "Sejuk", "Hangat", "Panas"], palette="Blues_r")
plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu pada data set bike_df")
plt.xlabel("Kategori Suhu")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.xticks(rotation=45)
st.pyplot(plt)
# Untuk dataset kedua (bike2_df), hitung rata-rata penyewaan per kategori suhu
avg_rentals_per_temp2 = bike2_df.groupby("temp_group2")["cnt"].mean().reset_index()

# Visualisasi menggunakan seaborn untuk dataset kedua
plt.figure(figsize=(8, 5))
sns.barplot(data=avg_rentals_per_temp2, x="temp_group2", y="cnt", order=["Dingin", "Sejuk", "Hangat", "Panas"], palette="Blues_r")
plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu Pada Data Set bike2_df")
plt.xlabel("Kategori Suhu")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.xticks(rotation=45)
st.pyplot(plt)
# Pertanyaan ke-2
st.write("*2.Pada jam berapa jumlah penyewaan sepeda mencapai puncaknya?*")

# Hitung total penyewaan sepeda untuk setiap jam
hourly_rentals = bike2_df.groupby("hr")["cnt"].sum().reset_index()

# Buat line chart
plt.figure(figsize=(10, 5))
sns.lineplot(data=hourly_rentals, x="hr", y="cnt", marker="o", color="b", linestyle="-")

# Atur label
plt.xlabel("Jam dalam Sehari (0-23)")
plt.ylabel("Total Penyewaan Sepeda")
plt.title("Jumlah Penyewaan Sepeda Berdasarkan Jam")

# Menampilkan sumbu x dari jam 0 sampai 23
plt.xticks(range(0, 24))  # Pastikan sumbu x menampilkan semua jam
plt.grid(True)  # Tambahkan grid agar lebih mudah dibaca

# Menampilkan grafik
st.pyplot(plt)