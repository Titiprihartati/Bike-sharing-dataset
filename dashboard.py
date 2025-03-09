{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMBqjKECdmdkc8GXBSweeFA",
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
        "\n",
        "# Load data dari GitHub\n",
        "bike_df = pd.read_csv(\"https://raw.githubusercontent.com/Titiprihartati/Bike-sharing-dataset/main/day.csv\")\n",
        "bike2_df = pd.read_csv(\"https://raw.githubusercontent.com/Titiprihartati/Bike-sharing-dataset/main/hour.csv\")\n",
        "\n",
        "# Konversi kolom tanggal\n",
        "bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])\n",
        "bike2_df['dteday'] = pd.to_datetime(bike2_df['dteday'])\n",
        "\n",
        "# Sidebar: Filter berdasarkan tanggal\n",
        "with st.sidebar:\n",
        "    st.image(\"https://github.com/dicodingacademy/assets/raw/main/logo.png\")\n",
        "    min_date = bike_df['dteday'].min()\n",
        "    max_date = bike_df['dteday'].max()\n",
        "    start_date, end_date = st.date_input(\"Periode Waktu\", [min_date, max_date],\n",
        "                                         min_value=min_date, max_value=max_date)\n",
        "\n",
        "# Filter data berdasarkan tanggal\n",
        "bike_df = bike_df[(bike_df['dteday'] >= pd.to_datetime(start_date)) &\n",
        "                  (bike_df['dteday'] <= pd.to_datetime(end_date))]\n",
        "bike2_df = bike2_df[(bike2_df['dteday'] >= pd.to_datetime(start_date)) &\n",
        "                    (bike2_df['dteday'] <= pd.to_datetime(end_date))]\n",
        "\n",
        "# --- Pertanyaan ke-1: Pengaruh Suhu terhadap Penyewaan Sepeda ---\n",
        "st.write(\"***1. Bagaimana pengaruh suhu terhadap jumlah sepeda yang disewa?***\")\n",
        "\n",
        "# Buat kategori suhu untuk kedua dataset dengan nama kolom yang sama\n",
        "bike_df[\"temp_group\"] = pd.qcut(bike_df[\"temp\"], q=4, labels=[\"Dingin\", \"Sejuk\", \"Hangat\", \"Panas\"])\n",
        "bike2_df[\"temp_group\"] = pd.qcut(bike2_df[\"temp\"], q=4, labels=[\"Dingin\", \"Sejuk\", \"Hangat\", \"Panas\"])\n",
        "\n",
        "# Analisis statistik berdasarkan suhu untuk bike_df\n",
        "temp_analysis = bike_df.groupby(\"temp_group\").agg({\n",
        "    \"cnt\": [\"mean\", \"median\", \"min\", \"max\", \"std\"],\n",
        "    \"registered\": [\"mean\", \"sum\"],\n",
        "    \"casual\": [\"mean\", \"sum\"]\n",
        "})\n",
        "st.write(temp_analysis)\n",
        "\n",
        "# Hitung rata-rata penyewaan per kategori suhu untuk bike_df\n",
        "avg_rentals_per_temp = bike_df.groupby(\"temp_group\")[\"cnt\"].mean().reset_index()\n",
        "\n",
        "# Visualisasi menggunakan seaborn untuk bike_df\n",
        "plt.figure(figsize=(8, 5))\n",
        "sns.barplot(data=avg_rentals_per_temp, x=\"temp_group\", y=\"cnt\",\n",
        "            order=[\"Dingin\", \"Sejuk\", \"Hangat\", \"Panas\"], palette=\"Blues_r\")\n",
        "plt.title(\"Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu (bike_df)\")\n",
        "plt.xlabel(\"Kategori Suhu\")\n",
        "plt.ylabel(\"Rata-rata Penyewaan Sepeda\")\n",
        "plt.xticks(rotation=45)\n",
        "plt.tight_layout()\n",
        "st.pyplot(plt)\n",
        "\n",
        "# Untuk dataset kedua (bike2_df), hitung rata-rata penyewaan per kategori suhu\n",
        "avg_rentals_per_temp2 = bike2_df.groupby(\"temp_group\")[\"cnt\"].mean().reset_index()\n",
        "\n",
        "# Visualisasi untuk bike2_df\n",
        "plt.figure(figsize=(8, 5))\n",
        "sns.barplot(data=avg_rentals_per_temp2, x=\"temp_group\", y=\"cnt\",\n",
        "            order=[\"Dingin\", \"Sejuk\", \"Hangat\", \"Panas\"], palette=\"Blues_r\")\n",
        "plt.title(\"Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu (bike2_df)\")\n",
        "plt.xlabel(\"Kategori Suhu\")\n",
        "plt.ylabel(\"Rata-rata Penyewaan Sepeda\")\n",
        "plt.xticks(rotation=45)\n",
        "plt.tight_layout()\n",
        "st.pyplot(plt)\n",
        "\n",
        "# --- Pertanyaan ke-2: Penyewaan Sepeda Berdasarkan Jam ---\n",
        "st.write(\"***2. Pada jam berapa jumlah penyewaan sepeda mencapai puncaknya?***\")\n",
        "\n",
        "# Hitung total penyewaan sepeda per jam dari bike2_df\n",
        "hourly_rentals = bike2_df.groupby(\"hr\")[\"cnt\"].sum().reset_index()\n",
        "\n",
        "plt.figure(figsize=(10, 5))\n",
        "sns.lineplot(data=hourly_rentals, x=\"hr\", y=\"cnt\", marker=\"o\", color=\"b\", linestyle=\"-\")\n",
        "plt.xlabel(\"Jam dalam Sehari (0-23)\")\n",
        "plt.ylabel(\"Total Penyewaan Sepeda\")\n",
        "plt.title(\"Jumlah Penyewaan Sepeda Berdasarkan Jam\")\n",
        "plt.xticks(range(0, 24))\n",
        "plt.grid(True)\n",
        "plt.tight_layout()\n",
        "st.pyplot(plt)\n",
        "\n",
        "# --- Analisis Regresi ---\n",
        "# Regresi: Pengaruh suhu terhadap penyewaan sepeda\n",
        "st.write(\"***Analisis regresi: Suhu vs Penyewaan Sepeda***\")\n",
        "combined_df = pd.concat([bike_df, bike2_df])\n",
        "X = combined_df[['temp']]\n",
        "X = sm.add_constant(X)\n",
        "y = combined_df['cnt']\n",
        "model = sm.OLS(y, X).fit()\n",
        "st.text(model.summary())\n",
        "\n",
        "# Regresi: Pengaruh jam terhadap penyewaan sepeda\n",
        "st.write(\"***Analisis regresi: Jam vs Penyewaan Sepeda***\")\n",
        "X_hr = bike2_df[['hr']]\n",
        "X_hr = sm.add_constant(X_hr)\n",
        "y_hr = bike2_df['cnt']\n",
        "model_hr = sm.OLS(y_hr, X_hr).fit()\n",
        "st.text(model_hr.summary())\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ReiFVqV5ybSp",
        "outputId": "74fa75c5-a3bf-4998-9789-895590d373d6"
      },
      "execution_count": 31,
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