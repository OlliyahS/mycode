import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO

'''
A couple of things to note about the data pulled from the CDC. 

1. It covers the period starting January 2018.

2. Due to COVID-19, there are data gaps between March 2020 and August 2020.

3.As of April 2nd, 2024, only 47 states and DC share data with the CDC's 
  Drug Overdose Surveillance and Epidemiology (DOSE) system.
  
4. States not participating include Texas, Wyoming, and North Dakota.

5. These charts specifically address non-fatal drug overdoses. 
   Fatal overdose data is reported by only 28 states to the CDC.

 
'''
def plot_graph(filtered_df):
    """
    Plot the DataFrame to a line graph and save it as an image file.
    """
    # Replace 'suppressed' values with NaN (not a number). This makes more sense when you look at the data set provided.   
    filtered_df = filtered_df.replace('suppressed', float('nan'))
    
    # Convert values to float for plotting
    for col in [filtered_df.columns[1], filtered_df.columns[2], filtered_df.columns[3]]:
        filtered_df[col] = pd.to_numeric(filtered_df[col], errors='coerce')


    # Convert values to float for plotting
    filtered_df.iloc[:, 1] = pd.to_numeric(filtered_df.iloc[:, 1], errors='coerce')
    
    
    # Plotting for the line graph
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df.iloc[:, 0], filtered_df.iloc[:, 1], color='green', label='Opioid')
    plt.plot(filtered_df.iloc[:, 0], filtered_df.iloc[:, 2], color='blue', label='Heroin')
    plt.plot(filtered_df.iloc[:, 0], filtered_df.iloc[:, 3], color='red', label='Stimulant')
    plt.xlabel('Months')  # x-axis label
    plt.ylabel('Percent in Change')  # y-axis label
    plt.title('Overdose Rates for Selected Year') #self explanatory
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig('plot.png')  # Saves the plot as a PNG file named "plot.png" 
    


# URL to the original Excel file from the CDC. Whenever they update this file, the information displayed in the graphs will update!
url = "https://www.cdc.gov/drugoverdose/nonfatal/dose/surveillance/dashboard/data/DOSE_dashboard_output-download.xlsx"

# Download the Excel file from the URL
try:
    response = requests.get(url) #sends a request to the URL link above to pull the exel file. 
    if response.status_code == 200: #if the get request is successful, perform this loop. 200 just indicates the request.get was successful
    #200 is the HTTP status code 
        excel_data = response.content # this reads the content of the Excel file from the URL
        
        # Read the Excel file from the content
        df = pd.read_excel(BytesIO(excel_data), engine='openpyxl', sheet_name="DOSE_dashboard_output-download", skiprows=5)
        
        # Prompt the user to enter a state code
        state_code = input("Enter a state code (e.g., AR, GA, CA, etc.): ").upper()
        
        # Filter the DataFrame based on the user input in the 1st column
        state_df = df[df.iloc[:, 0].str.contains(state_code)]
        
        # Filter state_df further to only include rows where the 24th row contains the string "7Month2MonthAR"
        state_df = state_df[state_df.iloc[:, 23].astype(str).str.contains("7Month2Month", na=False)]
        
        # Prompt the user to enter a year
        year = input("Enter a year: ")
        
        # Filter the existing DataFrame based on the user input in the 5th column (Year column)
        filtered_df = state_df[state_df.iloc[:, 4].astype(str).str.contains(year)]
        
        # Keep only the 5th, 10th, 11th, and 12th columns in the filtered DataFrame
        filtered_df = filtered_df.iloc[:, [5, 9, 10, 11]]
        
        plot_graph(filtered_df)
        print("Plot saved as 'plot.png'.")
        

        
    else:
        print("Failed to download the file. Status code:", response.status_code)

except Exception as e:
    print("Error:", e)
