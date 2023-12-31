import requests
import pandas as pd
import json

# Assuming you have a DataFrame named 'df' that you want to send
# Creating sample data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emma'],
    'Age': [25, 30, 35, 28, 32],
    'Gender': ['Female', 'Male', 'Male', 'Male', 'Female'],
    'City': ['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Miami']
}

# Creating a DataFrame
df = pd.DataFrame(data)

# Convert DataFrame to JSON format
df_json = df.to_json()

# Define the URL for the upload_dataframe endpoint
url = 'http://127.0.0.1:6030/upload_dataframe'

# Set headers to specify JSON content
headers = {'Content-Type': 'application/json'}

# Send a POST request to upload the DataFrame as JSON
response = requests.post(url, data=df_json, headers=headers)

# Check the response from the server
if response.status_code == 200:
    print('DataFrame uploaded successfully')
    
    # Convert the returned JSON data from the server to a DataFrame
    returned_data = response.json()
    if 'DataFrame' in returned_data:
        returned_df = pd.read_json(json.dumps(returned_data['DataFrame']))
        print('Returned Data from Server (as DataFrame):')
        print(returned_df)
    else:
        print('No DataFrame returned from the server')
else:
    print('Failed to upload DataFrame')



    