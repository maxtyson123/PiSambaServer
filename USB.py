import os
from PythonTools.debug import debug_message


def detect_usbs() -> list:
    """
    Detects all the USBs that are plugged into the server and returns them in a list

    @return: A list of usb devices and their mount points in an array following this structure: [[device, mount_point]] e.g. [["sda1", "/media/pi/USB"]]
    """
    debug_message("Detecting Usbs & their mount points")
    device_points = []
    mounted_usbs = []

    # GET THE USB DEVICES:
    command_output = os.popen('lsblk -d -o NAME,TRAN,MOUNTPOINT | grep usb').read().split("\n")
    for line in command_output:

        # Split the commands
        line_data = line.split(" ")

        # Remove all the elements that are empty
        line_data = [value for value in line_data if value != ""]

        # If there is no data then skip
        if len(line_data) < 1:
            continue

        # Add the device to the list
        device_points.append(line_data[0])

    # GET THE MOUNT POINTS:
    command_output = os.popen('lsblk -rno name,mountpoint').read().split("\n")
    for line_index in range(len(command_output)):

        # Split the commands
        line_data = command_output[line_index].split(" ")

        # Remove all the elemts that are empty
        if len(line_data) < 2:
            continue

        # Go through all the devices
        for device in device_points:

            # If the device is in the line and the mount point is not empty then add it to the list
            if device in line_data[0] and line_data[1] != "":
                mounted_usbs.append([line_data[0], line_data[1]])

    # DEBUG:
    for mountedUSB in mounted_usbs:
        debug_message(f"Usb: {mountedUSB[0]}. Mounted at: {mountedUSB[1]}")

    return mounted_usbs


def unmount_usb(mounted_usb: list) -> None:
    """
    Unmounts a USB from the server

    @param mounted_usb: The USB to unmount
    """

    # If the USB is not mounted then skip
    if "/External/" not in mounted_usb[1]:
        print(f"Usb: {mounted_usb[0]} is not mounted onto server, Skipping")
        return

    # Unmount the USB
    os.system(f"sudo umount {mounted_usb[1]}")
    debug_message(f"Unmounted: {mounted_usb[0]}")


def unmount_all(mounted_usbs: list) -> None:
    """
	Unmounts all the USBs from the server

    @param mounted_usbs: The USBs to unmount
    """
    for mountedUSB in mounted_usbs:
        unmount_usb(mountedUSB)


def mount_usb(mounted_usb: list) -> None:
    """
	Mounts a USB to the server

	@param mounted_usb: The USB to mount
	"""

    # If the USB is already mounted then skip
    if "/External/" in mounted_usb[1]:
        print(f"Usb: {mounted_usb[0]} is already mounted onto server, Skipping")
        return

    # List the folders in the External folder and increment the index (e.g. 01/, 02/, 03/ so make 04/)
    folders = os.listdir("/External/")
    usb_index = len(folders) + 1

    # Mount the USB
    os.system(f"sudo mkdir /External/0{usb_index}")
    os.system(f"sudo mount /dev/{mounted_usb[0]} /External/0{usb_index}")
    debug_message(f"Mounted /dev/{mounted_usb[0]} to /External/0{usb_index}")


def mount_all(mounted_usbs: list) -> None:
    """
	Mounts all the USBs to the server

	@param mounted_usbs: The USBs to mount
	"""
    for mountedUSB in mounted_usbs:
        mount_usb(mountedUSB)


def clean_folders() -> None:
    """
    Cleans the folders in the External folder for the hosting of the USBs
    """
    os.system("sudo rm -rf /External/*/")
