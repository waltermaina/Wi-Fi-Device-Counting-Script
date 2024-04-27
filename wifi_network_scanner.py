"""
Wi-Fi Device Counting Script

This script monitors the number of devices connected to a Wi-Fi network and plays a sound when it detects an increase
in the number of connected devices.

Usage:
- Ensure the Wi-Fi interface is active and connected to the desired network.
- Run this script to continuously monitor the number of connected devices.
"""

import re
import subprocess
import networkscan
from getmac import get_mac_address
from playsound import playsound
import time
import os

# Global variable to store the number of devices in the previous check
previous_count_of_connected = 0


def get_ipconfig_output():
    """
    Gets the ipconfig network command output.

    Returns:
        string: The output of the ipconfig command.
    """
    result = subprocess.run('ipconfig', stdout=subprocess.PIPE, text=True).stdout.lower()
    print(f"\n{result}")

    return result


def extract_wireless_info(ipconfig_output):
    """
    Extracts the IP address of the device and its gateway from the ipconfig command output.

    Args:
        ipconfig_output (string): The output of the ipconfig command.

    Returns:
        tuple: The ip address of the device and its gateway in that order, none if it is unable to get the address.
    """
    # Define a regular expression pattern to match IPv4 address and default gateway of wireless LAN adapter
    pattern = r"Wireless LAN adapter Wi.*?ipv4 address.*?: (\d+\.\d+\.\d+\.\d+).*?default gateway.*?: (\d+\.\d+\.\d+\.\d+)"

    # Search for the pattern in the provided IP configuration output
    match = re.search(pattern, ipconfig_output, re.IGNORECASE | re.DOTALL)
    if match:
        ipv4_address = match.group(1)
        default_gateway = match.group(2)
        return ipv4_address, default_gateway
    else:
        return None, None


def detect_wifi_network_and_count_devices(gateway_ip):
    """
    Detects the Wi-Fi network and counts the number of devices connected to the same Wi-Fi network as the device running the script.

    Args:
        gateway_ip (string): The IP address of the gateway.

    Returns:
        int: The number of devices connected to the Wi-Fi network.
    """

    # Define the network to scan
    # my_network = "192.168.43.0/24"  # sample Wi-Fi
    base_address_list = gateway_ip.split('.')
    my_network = f"{base_address_list[0]}.{base_address_list[1]}.{base_address_list[2]}.0/24"
    print(f"\nip range: {my_network}")

    # Create the object to scan the Wi-Fi network
    my_scan = networkscan.Networkscan(my_network)

    # Run the scan of hosts using pings
    my_scan.run()

    # Display the IP address of all the hosts found
    if len(my_scan.list_of_hosts_found) > 0:
        print("\nThe following devices were found on the network!")
        for device_ip in my_scan.list_of_hosts_found:
            # Get MAC address of device using ip address
            device_mac_address = get_mac_address(ip=device_ip)
            print(f"IP Address: {device_ip}     MAC Address: {device_mac_address}", flush=True)

        # Print the number of devices
        number_of_devices = len(my_scan.list_of_hosts_found)
        print(f"\nTotal devices detected: {number_of_devices}")

        # Show the number of devices minus the gateway too
        if gateway_ip in my_scan.list_of_hosts_found:
            print(f"\nTotal devices detected: {number_of_devices-1} if you remove gateway")
    else:
        print("\nNo devices found on the network!")

    return number_of_devices


def main():
    """
    The main function that continuously scans the network.
    """

    global previous_count_of_connected

    while True:
        try:
            # Get the ipconfig command output
            ipconfig_output = get_ipconfig_output()

            # Extract the IPv4 address and default gateway of the wireless LAN adapter
            ipv4_address, default_gateway = extract_wireless_info(ipconfig_output)

            # Do the network scan now
            if ipv4_address and default_gateway:
                print("IPv4 address of wireless LAN adapter:", ipv4_address)
                print("Default gateway of wireless LAN adapter:", default_gateway)

                # Get the number of devices on the network
                number_of_connected_devices = detect_wifi_network_and_count_devices(default_gateway)

                # Check if there was an increase in the number of devices
                if number_of_connected_devices > previous_count_of_connected:
                    try:
                        # Alert the owner by playing a sound, any other action can be taken here too

                        # Get the absolute path to the sound file
                        current_folder_path = os.getcwd()
                        siren_sound_path = f"{current_folder_path}\sounds\siren2.wav"
                        # print("Absolute path to current folder:", current_folder_path)
                        playsound(siren_sound_path)
                    except Exception as sound_error:
                        print(f"Sound error:{str(sound_error)}")

                previous_count_of_connected = number_of_connected_devices
            else:
                print("IPv4 address and/or default gateway not found for wireless LAN adapter.")
        except Exception as err:
            print(f"Error: {str(err)}")

        time.sleep(10)  # Delay for 10 seconds


if __name__ == "__main__":
    main()
