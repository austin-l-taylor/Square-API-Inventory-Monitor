# Square-API-Inventory-Monitor# Square Inventory Management System README

## Overview

This script is developed to work with Square's API for efficient inventory data management. It is capable of fetching inventory counts and catalog items, combining this data, and then exporting it to a CSV file. The script is designed to handle pagination in Square's API, managing large datasets effectively, and includes basic error handling capabilities.

## Features

- **Pagination Handling**: Retrieves inventory counts and catalog items from Square's API, managing large data sets with ease.
- **Data Combination**: Combines inventory data with catalog items for a complete inventory overview.
- **CSV Export**: Outputs the combined data into a CSV file for easy access and manipulation.
- **Error Handling**: Captures and logs errors to a file, aiding in troubleshooting and maintenance.

## Requirements

- Python 3
- `square` Python package
- Valid Square API access token

## Installation

1. Ensure Python 3 is installed.
2. Install the `square` package using pip:

    ```bash
    pip install squareup
    ```

## Usage

Run the script via the command line, providing the Square API access token as an argument:

```bash
python script_name.py [ACCESS_TOKEN]
