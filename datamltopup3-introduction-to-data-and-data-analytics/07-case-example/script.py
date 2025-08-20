import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
dim_building = pd.read_csv('DimBuilding.csv')
dim_meter = pd.read_csv('DimMeter.csv')
dim_weather = pd.read_csv('DimWeatherStation.csv')
fact_meter = pd.read_csv('FactMeterData.csv')
fact_weather = pd.read_csv('FactWeatherData.csv')

# Display first few rows
print(dim_building.head())
print(dim_meter.head())
print(dim_weather.head())
print(fact_meter.head())
print(fact_weather.head())

# Merge building data with meter
meter_building = dim_meter.merge(dim_building, on="building_id")

# Merge consumption data with meter-building
meter_data = fact_meter.merge(meter_building, on="meter_id")

# Merge with weather data via weather station
weather_data = fact_weather.merge(dim_weather, on="fmis_id")

# Merge meter and weather time series data
full_data = meter_data.merge(weather_data, on=["weatherstation_id", "datetime"])

# Filter subsets of data from analysis
heating_data = full_data[full_data["meter_type"] == "Heating"]
electricity_data = full_data[full_data["meter_type"] == "Electricity"]

# Convert datetime column to pandas datetime format
heating_data["datetime"] = pd.to_datetime(heating_data["datetime"])
electricity_data["datetime"] = pd.to_datetime(electricity_data["datetime"])

# Extract hour and weekday 
heating_data["hour_of_day"] = heating_data["datetime"].dt.hour
heating_data["day_of _week"] = heating_data["datetime"].dt.dayofweek

electricity_data["hour_of_day"] = electricity_data["datetime"].dt.hour 
electricity_data["day_of_week"] = electricity_data["datetime"].dt.dayofweek

# Sort data with datetime column 
heating_data = heating_data.sort_values(by=['datetime'])
electricity_data = electricity_data.sort_values(by=['datetime']) 

# Print dataframes 
print(heating_data)
print(electricity_data)

# Check for missing values
print(heating_data.isnull().sum()) 
print(electricity_data.isnull().sum())

# Drop rows with missing values
heating_data = heating_data.dropna()
electricity_data = electricity_data.dropna()

# Plot Consumption vs Air Temperature
plt.figure(figsize=(8, 6))
sns.scatterplot(x=heating_data["air_temperature"], y=heating_data["consumption"], alpha=0.5)
plt.xlabel("Air Temperature (°C)")

plt.ylabel("Heating Consumption")
plt.title("Heating Consumption vs Air Temperature")
plt.show()