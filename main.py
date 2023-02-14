import csv
import math
import Levenshtein # Module to check if the names are similar
import pandas as pd

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude to spherical coordinates in radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula to calculate the great-circle distance between two points on a sphere
    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2-lon1)/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371 # Radius of earth in kilometers
    return c * r * 1000 # Convert to meters

# Read the data into a list of dictionaries
data = []
with open("assignment_data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

# Create a new column to store the results of the comparison
for row in data:
    row["is_similar"] = 0

# Loop over each entry and compare it to all other entries
for i in range(len(data)):
    for j in range(i+1, len(data)):
        # Check if the distance is less than 200 meters
        distance = haversine_distance(float(data[i]["latitude"]), float(data[i]["longitude"]),
                                      float(data[j]["latitude"]), float(data[j]["longitude"]))
        if distance < 200:
            # Check if the names are similar
            name1 = data[i]["name"]
            name2 = data[j]["name"]
            if Levenshtein.distance(name1, name2) < 5:
                # Mark both entries as similar
                data[i]["is_similar"] = 1
                data[j]["is_similar"] = 1

# Write the results to a new CSV file
fields = ["name","lat", "lon", "is_similar"]
with open("output.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for row in data:
        row_output = {"name": row["name"], "lat": row["latitude"], "lon": row["longitude"],
                      "is_similar": row["is_similar"]}
        writer.writerow(row_output)

# Remove extra blank row fromt the whole csv file
df = pd.read_csv('output.csv')
new_df = df.dropna()
new_df.to_csv('output.csv', index=False)
