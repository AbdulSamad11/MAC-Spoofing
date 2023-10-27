import subprocess
import atexit
import re

def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
        mac_address_search_result = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", ifconfig_result)
        if mac_address_search_result:
            return mac_address_search_result.group(0)
    except subprocess.CalledProcessError:
        pass
    return None

def change_mac(interface, new_mac):
    print(f"Changing MAC address of {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def revert_mac(interface, original_mac):
    print(f"Reverting MAC address of {interface} to {original_mac}")
    change_mac(interface, original_mac)

def main():
    interface = "your_wifi_interface"  # Replace with your Wi-Fi interface name, e.g., wlan0

    # Store the current MAC address
    original_mac = get_current_mac(interface)
    if not original_mac:
        print("Unable to read the original MAC address. Exiting.")
        return

    print(f"Original MAC address of {interface}: {original_mac}")

    new_mac = "00:11:22:33:44:55"  # Replace with the new MAC address you want to use

    change_mac(interface, new_mac)

    # Register a function to revert MAC address when the program exits
    atexit.register(revert_mac, interface, original_mac)

    try:
        # Your program logic goes here
        # For example, you can run your assignment-related code here
        # The MAC address will automatically revert when the program exits

        input("Press Enter to stop the program...")

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
