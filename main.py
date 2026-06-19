import requests
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os

API_KEY = os.getenv("API_KEY")

symbols = [("EUR", "USD")]

all_data = []

for from_sym, to_sym in symbols:
    print(f"Descargando {from_sym}/{to_sym}...")

    url = (
        "https://www.alphavantage.co/query"
        f"?function=FX_DAILY"
        f"&from_symbol={from_sym}"
        f"&to_symbol={to_sym}"
        f"&outputsize=full"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    json_data = response.json()

    time_series = json_data.get("Time Series FX (Daily)", None)

    if not time_series:
        print("ERROR API:")
        print(json_data)
        continue

    df = pd.DataFrame.from_dict(time_series, orient="index")
    df.index = pd.to_datetime(df.index)

    df = df.rename(columns={
        "1. open": "open",
        "4. close": "close"
    })[["open", "close"]]

    all_data.append(df)

if not all_data:
    print("Sin datos.")
    exit()

data = pd.concat(all_data)
data = data.sort_index()

data.index.name = "Fecha"

print("Precios diarios de Forex:\n")
print(data.tail())

print("\nCorrelación:")
print(data[["open", "close"]].corr())

data.to_csv("20.csv")

print("\nArchivo guardado como '20.csv'")
