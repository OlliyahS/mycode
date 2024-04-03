import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO

def plot_graph(filtered_df):
    """
    Plot the DataFrame to a bar graph and save it as an image file.
    """
    # Replace 'suppressed' values with NaN (not a number). This makes more sense when you look at the data set provided.   
    filtered_df = filtered_df.replace('suppressed', float('nan'))
    
    # Convert values to float for plotting
    filtered_df.iloc[:, 1] = pd.to_numeric(filtered_df.iloc[:, 1], errors='coerce')


    # Plotting for the bar graph
    plt.figure(figsize=(10, 6))
    sns.barplot(x=filtered_df.iloc[:, 0], y=filtered_df.iloc[:, 1], color='hotpink')  # Use Seaborn barplot function and makes it look pretty in pink
    plt.xlabel('Months')  # x-axis label
    plt.ylabel('Percent Increase/Decrease')  # y-axis label
    plt.title('Bar Graph for Opioid Overdose Rates for Selected Year') #self explanatory
    plt.xticks(rotation=45, ha='right')
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
        
        # Keep only the 5th and 11th columns in the filtered DataFrame
        filtered_df = filtered_df.iloc[:, [5, 9]]
        
        plot_graph(filtered_df)
        print("Plot saved as 'plot.png'.")
        

        
    else:
        print("Failed to download the file. Status code:", response.status_code)

except Exception as e:
    print("Error:", e)
