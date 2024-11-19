import json

# Data to be printed
data = {'weatherObservation': {'elevation': 432, 'lng': 8.533333333333333, 'observation': 'LSZH 270420Z AUTO 05002KT 9999 3400NW NCD M02/M02 Q1023 BECMG 3000', 'ICAO': 'LSZH', 'clouds': 'no clouds detected', 'dewPoint': '-2', 'cloudsCode': 'NCD', 'datetime': '2023-12-27 04:20:00', 'countryCode': 'CH', 'temperature': '-2', 'humidity': 100, 'stationName': 'Zurich-Kloten', 'weatherCondition': 'n/a', 'windDirection': 50, 'hectoPascAltimeter': 1023, 'windSpeed': '02', 'lat': 47.483333333333334}, 'id': 22}

# Convert to a single-line JSON string
json_string = json.dumps(data, separators=(',', ':'))

# Print the JSON string to the console for 100 lines
for _ in range(100):
    print(json_string)

print("Data printed to console")
