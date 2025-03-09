{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNhBLqOPuHROS4FsKyKr20p",
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
        "# Analisis suhu dan jumlah penyewaan\n",
        "st.subheader(\"📊 Analisis Pengaruh Suhu terhadap Penyewaan Sepeda\")\n",
        "\n",
        "bike_df[\"temp_group\"] = pd.qcut(bike_df[\"temp\"], q=4, labels=[\"Dingin\", \"Sejuk\", \"Hangat\", \"Panas\"])\n",
        "avg_rentals_per_temp = bike_df.groupby(\"temp_group\")[\"cnt\"].mean().reset_index()\n",
        "\n",
        "fig, ax = plt.subplots()\n",
        "sns.barplot(data=avg_rentals_per_temp, x=\"temp_group\", y=\"cnt\", palette=\"Blues_r\", ax=ax)\n",
        "ax.set_title(\"Rata-rata Penyewaan Sepeda Berdasarkan Suhu\")\n",
        "ax.set_xlabel(\"Kategori Suhu\")\n",
        "ax.set_ylabel(\"Rata-rata Penyewaan Sepeda\")\n",
        "st.pyplot(fig)\n",
        "\n",
        "# Analisis jam penyewaan sepeda\n",
        "st.subheader(\"⏰ Jam Tersibuk dalam Penyewaan Sepeda\")\n",
        "\n",
        "if \"hr\" in bike2_df.columns:\n",
        "    hourly_rentals = bike2_df.groupby(\"hr\")[\"cnt\"].sum().reset_index()\n",
        "    fig, ax = plt.subplots()\n",
        "    sns.lineplot(data=hourly_rentals, x=\"hr\", y=\"cnt\", marker=\"o\", color=\"b\", linestyle=\"-\", ax=ax)\n",
        "    ax.set_title(\"Jumlah Penyewaan Sepeda Berdasarkan Jam\")\n",
        "    ax.set_xlabel(\"Jam dalam Sehari (0-23)\")\n",
        "    ax.set_ylabel(\"Total Penyewaan Sepeda\")\n",
        "    ax.grid(True)\n",
        "    st.pyplot(fig)\n",
        "else:\n",
        "    st.write(\"Kolom 'hr' tidak ditemukan di bike2_df!\")\n",
        "\n",
        "# Analisis regresi\n",
        "st.subheader(\"📉 Analisis Regresi: Suhu vs Penyewaan Sepeda\")\n",
        "\n",
        "X = bike_df[['temp']]\n",
        "X = sm.add_constant(X)\n",
        "y = bike_df['cnt']\n",
        "model = sm.OLS(y, X).fit()\n",
        "st.text(model.summary())\n",
        "\n",
        "st.subheader(\"📉 Analisis Regresi: Jam vs Penyewaan Sepeda\")\n",
        "\n",
        "if \"hr\" in bike2_df.columns:\n",
        "    X = bike2_df[['hr']]\n",
        "    X = sm.add_constant(X)\n",
        "    y = bike2_df['cnt']\n",
        "    model = sm.OLS(y, X).fit()\n",
        "    st.text(model.summary())\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ReiFVqV5ybSp",
        "outputId": "eb69876a-0a09-4612-f5e7-39356746817b"
      },
      "execution_count": 29,
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