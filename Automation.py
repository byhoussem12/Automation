import os
import requests
import re
import logging
import pandas as pd
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime

# Get the directory where the script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Configure logging to save to the same folder as the script
log_file = os.path.join(base_dir, 'Automation.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file
)

# Function to retrieve and process data from Eurocontrol
def retrieve_data():
    """
    Fetch daily traffic variation data from Eurocontrol, process it, and save it as a CSV file.
    Returns:
        dict: A dictionary with success or error message.
    """
    try:
        logging.info("Starting data retrieval process.")
        print("Starting data retrieval...")

        # URL of the page containing the download button
        page_url = "https://www.eurocontrol.int/Economics/DailyTrafficVariation-States.html"
        response = requests.get(page_url)
        
        if response.status_code != 200:
            error_msg = f"Failed to fetch the page. Status code: {response.status_code}"
            logging.error(error_msg)
            return {"error": error_msg}

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the script tag that contains the download URL
        script_tags = soup.find_all('script')
        download_url = None
        for script in script_tags:
            if script.string and 'ButtonDownload' in script.string:
                match = re.search(r'link\.href\s*=\s*"([^"]+)"', script.string)
                if match:
                    download_url = match.group(1)
                    break

        if not download_url:
            error_msg = "No download URL found in the JavaScript."
            logging.error(error_msg)
            return {"error": error_msg}

        # Load the Excel file from the download URL
        excel_file = pd.ExcelFile(download_url)
        
        # Find a sheet that contains 'data' in its name
        data_sheet = next((sheet for sheet in excel_file.sheet_names if 'data' in sheet.lower()), None)
        if not data_sheet:
            error_msg = "No sheet containing 'data' found."
            logging.error(error_msg)
            return {"error": error_msg}

        # Load the data into a DataFrame
        df = pd.read_excel(excel_file, sheet_name=data_sheet)

        # Save the CSV file in the same directory as the script
        output_dir = os.path.join(base_dir, 'processed_data')
        os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
        output_file = os.path.join(output_dir, 'processed_data.csv')
        df.to_csv(output_file, index=False)

        logging.info(f"Data saved to {output_file}")
        print(f"Data saved to: {output_file}")
        return {"message": f"Data saved to {output_file}"}

    except requests.exceptions.RequestException as e:
        error_msg = f"Network error occurred: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
        return {"error": error_msg}

# Mock AWS Lambda Context class (for simulating Lambda environment)
class MockContext:
    def __init__(self):
        self.aws_request_id = "123456"
        self.function_name = "retrieve_data"
        self.memory_limit_in_mb = 128

# Simulate Lambda event and context
event = {}  # Empty event for simplicity, can be populated if needed
context = MockContext()

# Function to simulate the scheduler
def schedule_lambda():
    """
    Schedule the retrieve_data function to run periodically (e.g., every 1 minute for testing).
    """
    schedule.every(24).hour.do(lambda: retrieve_data())
    logging.info("Scheduler is running. Press Ctrl+C to stop.")
    print("Scheduler is running. Press Ctrl+C to stop.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Main execution block to test and run everything
if __name__ == "__main__":

    # Now, start the scheduler to call the retrieve_data periodically
    schedule_lambda()
