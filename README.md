# Eurocontrol Daily Traffic Variation Data Automation

## Overview

This project automates the retrieval, processing, and storage of air traffic variation data from the Eurocontrol website. It simulates a cloud-based infrastructure locally using mock setups and scheduling libraries.

Key functionalities include:
- Downloading and processing air traffic data into a structured CSV format.
- Simulating a cloud environment for local testing.
- Scheduling periodic tasks for automation.

---

## Features

1. **Data Retrieval**: Automatically fetches daily traffic variation data from the Eurocontrol website.
2. **Data Processing**: Extracts relevant information and converts it into a structured CSV format.
3. **Automation**: Runs periodically (every 24 hours) using a local scheduler.
4. **Infrastructure Simulation**: 
   - **Mock AWS Lambda Context**: Simulates a cloud environment for local testing.
   - **SST Alternative**: Initially considered but replaced due to dependency issues.
5. **Error Handling and Logging**: Tracks successes and errors in a log file for debugging and monitoring.

---

## Requirements

### Prerequisites

1. **Python**: Version 3.8 or higher.
2. **Python Libraries**: Install the following dependencies:
   ```bash
   pip install requests beautifulsoup4 pandas openpyxl schedule
   ```
---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/byhoussem12/Automation.git
   cd Automation
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure all necessary libraries are installed.)*

3. **Run the Script**:
   ```bash
   python lambda_simulation.py
   ```
   The script will:
   - Fetch and process Eurocontrol traffic data.
   - Save the processed data as a CSV file in the `./processed_data` directory.

4. **Check Logs**:
   Execution details and errors will be logged in `lambda_simulation.log`.

---

## File Structure

```
Automation/
├── lambda_simulation.py       # Main script for data retrieval and processing
├── processed_data/            # Directory for saving processed CSV files
├── lambda_simulation.log      # Log file for tracking execution status
├── README.md                  # Project documentation
└── requirements.txt           # List of Python dependencies
```

---

## Automation Simulation

The script uses the `schedule` library to automate data retrieval and processing. By default, it runs every 24 hours. To modify the interval, update the following line in `lambda_simulation.py`:

```python
schedule.every(24).hours.do(lambda: retrieve_data())
```

Run the script in an interactive terminal, and press `Ctrl+C` to stop it.

---

## Infrastructure Simulation

### Mock Lambda Setup

- **Attributes Mimicking Lambda**:
  - `aws_request_id`: Unique identifier for each Lambda invocation.
  - `function_name`: Simulates the Lambda function's name.
  - `memory_limit_in_mb`: Mimics AWS Lambda's memory constraints.
  
- **Usage**:
  The `MockContext` class is instantiated within the script to simulate AWS Lambda locally. An empty `event` dictionary is passed for controlled testing.

- **Benefits**:
  - Simplifies local testing and debugging.
  - Avoids dependency on external tools or cloud resources.

### SST Alternative

Initially, SST (Serverless Stack Toolkit) was considered for infrastructure simulation. However, unresolved dependency issues led to the adoption of the mock setup for seamless local testing.

---

## Future Deployment in the Cloud

This project can be extended to the cloud as follows:

1. **AWS Lambda**:
   - Package the script and deploy it as a Lambda function.

2. **AWS EventBridge**:
   - Schedule periodic executions of the Lambda function.

3. **AWS S3**:
   - Store processed CSV files in an S3 bucket for centralized access.

4. **Cloud Logging**:
   - Use AWS CloudWatch for monitoring and debugging.

---

## Processed Data Example

After running the script, the processed data is saved in the `./processed_data` directory. The CSV files contain structured information extracted from the Eurocontrol dataset, ready for further analysis.

---

## Known Issues

- **SST Dependencies**: Could not resolve issues, leading to reliance on a mock infrastructure setup.
