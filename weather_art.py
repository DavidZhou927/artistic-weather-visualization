import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 1. Get weather data from Open-Meteo API
def fetch_weather_data(latitude, longitude, days=7):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&start_date={start_date}&end_date={end_date}"
        "&hourly=temperature_2m,relative_humidity_2m,windspeed_10m"
        "&timezone=auto"
    )
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame({
        "time": data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"],
        "humidity": data["hourly"]["relative_humidity_2m"],
        "windspeed": data["hourly"]["windspeed_10m"]
    })
    df["time"] = pd.to_datetime(df["time"])
    return df

# 2. Data cleaning and processing
def clean_weather_data(df):
    df = df.dropna()
    df = df[(df["temperature"] > -50) & (df["temperature"] < 60)]
    # Normalize to 0-1
    for col in ["temperature", "humidity", "windspeed"]:
        mn, mx = df[col].min(), df[col].max()
        df[col+"_norm"] = (df[col] - mn) / (mx - mn)
    return df

# 3. Artistic visualization
def artistic_visualization(df, save_path="weather_art.png"):
    plt.figure(figsize=(12, 6), dpi=120)
    t = np.linspace(0, 2*np.pi, len(df))

    # Generate parameters based on temperature, humidity, and wind speed
    r = 1 + df["temperature_norm"].values * 2
    theta = t + df["humidity_norm"].values * np.pi
    colors = plt.cm.viridis(df["windspeed_norm"].values)

    # Polar coordinate abstract painting
    ax = plt.subplot(1, 1, 1, polar=True)
    ax.set_facecolor('black')
    c = ax.scatter(theta, r, c=colors, s=100*df["windspeed_norm"].values+20, alpha=0.7)

    # Fusion curve
    curve = r * np.sin(3*theta + df["windspeed_norm"].values * np.pi)
    ax.plot(theta, curve, color="cyan", alpha=0.4, lw=2)
    
    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Weather Art: Temperature, Humidity, Wind", color="white", fontsize=16)
    plt.savefig(save_path, bbox_inches="tight", facecolor='black')
    plt.show()

if __name__ == "__main__":
    # Taking Beijing as an example (can be replaced with other city coordinates)
    latitude, longitude = 39.9042, 116.4074
    print("Fetching data...")
    df = fetch_weather_data(latitude, longitude, days=7)
    df = clean_weather_data(df)
    artistic_visualization(df)