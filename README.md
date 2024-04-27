# Wi-Fi Device Counting Script

This Python script monitors the number of devices connected to a Wi-Fi network and plays a sound when it detects an increase in the number of connected devices.

## Prerequisites

Before setting up the script, ensure you have the following:
- `pipenv` installed
- Python version `3.10` installed (if not, edit the python version in the `Pipfile`)

## Setup

To set up the script, follow these steps:

1. Run the `pipenv shell` command to spawn a shell within the virtual environment.
2. Run the `pipenv install` command to install all required packages.
3. Run the script with the command `python wifi_network_scanner.py`.

## Compatibility

The script has been tested on Windows and is not guaranteed to work on Linux.

## Usage

Ensure the Wi-Fi interface is active and connected to the desired network, then run this script to continuously monitor the number of connected devices.

## Note

This script requires administrative privileges to run on some systems due to the network scanning functionality. Please ensure you have the necessary permissions before executing the script.
