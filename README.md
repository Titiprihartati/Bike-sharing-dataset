%%writefile README.md
# Dicoding Collection Dashboard ✨
Proyek ini bertujuan untuk menganalisis data penyewaan sepeda

# Setup Environment - Anaconda
conda create --name bike-analysis python=3.9
conda activate bike-analysis
pip install -r requirements.txt

## Setup Environment - Shell/Terminal
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.tx

## Run steamlit app
streamlit run dashboard.py

# Struktur Direktori
submission
dashboard
main_data.csv
dashboard.py
data
data_1.csv
data_2.csv
notebook.ipynb
README.md
requirements.txt
url.txt
