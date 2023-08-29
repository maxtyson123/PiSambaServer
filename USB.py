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
        debug_message(f"Found Device: {line_data[0]}")
        device_points.append(line_data[0])

    # GET THE MOUNT POINTS:
    command_output = os.popen('lsblk -rno name,mountpoint').read().split("\n")
    for line_index in range(len(command_output)):

        # Split the commands
        line_data = command_output[line_index].split(" ")

        # Go through all the devices
        for device in device_points:

            # If the device is in the line (but is not the device it self) and the mount point is not empty then add it to the list
            if device in line_data[0] and device != line_data[0]:
                mounted_usbs.append([line_data[0], line_data[1]])

    # DEBUG:
    for mountedUSB in mounted_usbs:
        debug_message(f"Usb: {mountedUSB[0]}. Mounted at: {mountedUSB[1]}")

    return mounted_usbs

def check_mounted(mounted_usb: list) -> None:
  return "/External" in mounted_usb[1]

def unmount_usb(mounted_usb: list) -> None:
    """
    Unmounts a USB from the server

    @param mounted_usb: The USB to unmount
    """

    # If the USB is not mounted then skip
    if not check_mounted(mounted_usb):
        debug_message(f"Usb: {mounted_usb[0]} is not mounted onto server, Skipping")
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
    if check_mounted(mounted_usb):
        debug_message(f"Usb: {mounted_usb[0]} is already mounted onto server, Skipping")
        return

    # List the folders in the External folder and increment the index (e.g. 01/, 02/, 03/ so make 04/)
    folders = os.listdir("/External/")
    usb_index = 0

    # Find an unused index
    while f"0{usb_index}" in folders:
       debug_message(f"0{usb_index} in folder")
       usb_index += 1

    # Mount the USB
    os.system(f"sudo mkdir /External/0{usb_index}")
    os.system(f"sudo mount -o rw,user,uid=1000,umask=007,exec /dev/{mounted_usb[0]} /External/0{usb_index}")
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
    os.system("find /External/ -type d -empty -delete")
    command_output = os.popen('ls /External').read().split("\n")
    debug_message(f"Folders Left: {', '.join(command_output)}")
