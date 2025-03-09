{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNBJPR/1+QD656OPyry+4ks",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Titiprihartati/Bike-sharing-dataset/blob/main/dashboard.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile dashboard.py\n",
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "import statsmodels.api as sm\n",
        "\n",
        "sns.set(style='dark')\n",
        "\n",
        "st.title(\"🚴‍♂️ Dashboard Analisis Penyewaan Sepeda🚴‍♂️\")\n",
        "st.write(\"by: Titi Prihartati\")\n",
        "bike_df = pd.read_csv(\"https://raw.githubusercontent.com/Titiprihartati/Bike-sharing-dataset/main/day.csv\")\n",
        "bike2_df = pd.read_csv(\"https://raw.githubusercontent.com/Titiprihartati/Bike-sharing-dataset/main/hour.csv\")\n",
        "bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])\n",
        "bike2_df['dteday'] = pd.to_datetime(bike2_df['dteday'])\n",
        "\n",
        "# Sidebar untuk filter tanggal\n",
        "with st.sidebar:\n",
        "    st.image(\"https://github.com/dicodingacademy/assets/raw/main/logo.png\")\n",
        "\n",
        "    min_date = bike_df['dteday'].min()\n",
        "    max_date = bike_df['dteday'].max()\n",
        "\n",
        "    start_date, end_date = st.date_input(\"Periode Waktu\", [min_date, max_date], min_value=min_date, max_value=max_date)\n",
        "\n",
        "# Filter data berdasarkan tanggal\n",
        "bike_df = bike_df[(bike_df['dteday'] >= pd.to_datetime(start_date)) & (bike_df['dteday'] <= pd.to_datetime(end_date))]\n",
        "bike2_df = bike2_df[(bike2_df['dteday'] >= pd.to_datetime(start_date)) & (bike2_df['dteday'] <= pd.to_datetime(end_date))]\n",
        "\n",
        "# Pertanyaan ke-1\n",
        "st.write(\"***1. Bagaimana pengaruh suhu terhadap jumlah sepeda yang disewa?***\")\n",
        "\n",
        "# Grouping berdasarkan suhu (dibagi dalam interval)\n",
        "bike_df[\"temp_group\"] = pd.qcut(bike_df[\"temp\"], q=4, labels=[\"Dingin\", \"Sejuk\", \"Hangat\", \"Panas\"])\n",
        "\n",
        "# Analisis statistik berdasarkan suhu\n",
        "temp_analysis = bike_df.groupby(\"temp_group\").agg({\n",
        "    \"cnt\": [\"mean\", \"median\", \"min\", \"max\", \"std\"],\n",
        "    \"registered\": [\"mean\", \"sum\"],\n",
        "    \"casual\": [\"mean\", \"sum\"]\n",
        "})\n",
        "\n",
        "# Tampilkan hasil analisis suhu\n",
        "temp_analysis\n",
        "\n",
        "# Hitung rata-rata penyewaan per kategori suhu\n",
        "avg_rentals_per_temp = bike_df.groupby(\"temp_group\")[\"cnt\"].mean().reset_index()\n",
        "\n",
        "# Visualisasi menggunakan seaborn\n",
        "plt.figure(figsize=(8, 5))\n",
        "sns.barplot(data=avg_rentals_per_temp, x=\"temp_group\", y=\"cnt\", order=[\"Dingin\", \"Sejuk\", \"Hangat\", \"Panas\"], palette=\"Blues_r\")\n",
        "plt.title(\"Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu pada data set bike_df\")\n",
        "plt.xlabel(\"Kategori Suhu\")\n",
        "plt.ylabel(\"Rata-rata Penyewaan Sepeda\")\n",
        "plt.xticks(rotation=45)\n",
        "plt.show()\n",
        "\n",
        "# Untuk dataset kedua (bike2_df), hitung rata-rata penyewaan per kategori suhu\n",
        "avg_rentals_per_temp2 = bike2_df.groupby(\"temp_group2\")[\"cnt\"].mean().reset_index()\n",
        "\n",
        "# Visualisasi menggunakan seaborn untuk dataset kedua\n",
        "plt.figure(figsize=(8, 5))\n",
        "sns.barplot(data=avg_rentals_per_temp2, x=\"temp_group2\", y=\"cnt\", order=[\"Dingin\", \"Sejuk\", \"Hangat\", \"Panas\"], palette=\"Blues_r\")\n",
        "plt.title(\"Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu Pada Data Set bike2_df\")\n",
        "plt.xlabel(\"Kategori Suhu\")\n",
        "plt.ylabel(\"Rata-rata Penyewaan Sepeda\")\n",
        "plt.xticks(rotation=45)\n",
        "plt.show()\n",
        "\n",
        "# Pertanyaan ke-2\n",
        "st.write(\"***2.Pada jam berapa jumlah penyewaan sepeda mencapai puncaknya?***\")\n",
        "\n",
        "# Hitung total penyewaan sepeda untuk setiap jam\n",
        "hourly_rentals = bike2_df.groupby(\"hr\")[\"cnt\"].sum().reset_index()\n",
        "\n",
        "# Buat line chart\n",
        "plt.figure(figsize=(10, 5))\n",
        "sns.lineplot(data=hourly_rentals, x=\"hr\", y=\"cnt\", marker=\"o\", color=\"b\", linestyle=\"-\")\n",
        "\n",
        "# Atur label\n",
        "plt.xlabel(\"Jam dalam Sehari (0-23)\")\n",
        "plt.ylabel(\"Total Penyewaan Sepeda\")\n",
        "plt.title(\"Jumlah Penyewaan Sepeda Berdasarkan Jam\")\n",
        "\n",
        "# Menampilkan sumbu x dari jam 0 sampai 23\n",
        "plt.xticks(range(0, 24))  # Pastikan sumbu x menampilkan semua jam\n",
        "plt.grid(True)  # Tambahkan grid agar lebih mudah dibaca\n",
        "\n",
        "# Menampilkan grafik\n",
        "plt.show()\n",
        "\n",
        "# Analisis Lanjutan\n",
        "st.write(\"***Analisis regresi untuk melihat apakah suhu mempengaruhi jumlah sepeda yang di sewa ***\")\n",
        "\n",
        "combined_df = pd.concat([bike_df, bike2_df])\n",
        "X = combined_df[['temp']]\n",
        "x = sm.add_constant(X)  # Tambah konstanta untuk model regresi\n",
        "y = combined_df['cnt']\n",
        "model = sm.OLS(y, X).fit()\n",
        "print(model.summary())\n",
        "\n",
        "# Analisis Lanjutan\n",
        "st.write(\"***Analisis regresi untuk melihat apakah jam mempengaruhi jumlah sepeda yang di sewa ***\")\n",
        "\n",
        "# Variabel independen (jam)\n",
        "X = bike2_df[['hr']]\n",
        "X = sm.add_constant(X)  # Tambahkan konstanta\n",
        "\n",
        "# Variabel dependen (jumlah penyewa)\n",
        "y = bike2_df['cnt']\n",
        "\n",
        "# Model regresi\n",
        "model = sm.OLS(y, X).fit()\n",
        "\n",
        "# Hasil regresi\n",
        "print(model.summary())"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ReiFVqV5ybSp",
        "outputId": "368245cb-506c-428a-e149-834d24396c89"
      },
      "execution_count": 30,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Overwriting dashboard.py\n"
          ]
        }
      ]
    }
  ]
}