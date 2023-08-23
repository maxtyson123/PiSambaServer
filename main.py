import os
import sys

from PythonTools.debug import debug_message, init_debug, close_debug_session, handle_arg
from PythonTools.files import UserData
from PythonTools.network import get_ip
from PythonTools.renderer import Menu, clear, render_text, get_input, init_gui, gui_close
from PythonTools.tools import string_bool, ip_address
from USB import detect_usbs, unmount_all, mount_all, clean_folders, unmount_usb


def main() -> None:
    """
    The main function, initialise the program and show the main menu
    """


    # Loop until stopped
    while True:
        item_names = ["Refresh USBs", "Close Server"]
        item_values = [
                        '<i class="fa-solid fa-rotate" style="font-size: 24px"></i>',
                        '<i class="fa-solid fa-circle-xmark" style="font-size: 24px"></i>'
                      ]

        # Detect the USBs
        mounted_usbs = detect_usbs()

        # Add them after the refresh button
        for usb in mounted_usbs:
            item_names.append(f"{usb[0]} | {usb[1]}")
            item_values.append('<i class="fa-solid fa-eject" style="font-size: 24px"></i>')

        menu_items = [item_names, item_values]
        main_menu = Menu(f"SAMBA Server: {get_ip()}/RaspberryPI", menu_items, True)

        user_input = main_menu.get_input()

        # Check if the user refreshed the USBs or closed the server
        match user_input:
            case "Refresh USBs":
                continue

            case "Close Server":
                break

        # User must have selected a USB to unmount

        # Fin the USB to unmount
        for usb in mounted_usbs:

            # Check if the device name is in the user input
            if usb[0] in user_input:

                # Unmount the USB
                unmount_usb(usb)
                break

def init_main() -> None:
    # Detect the USBs
    mounted_usbs = detect_usbs()

    # Un Mount any old USBs
    unmount_all(mounted_usbs)

    # Clean the External folder
    clean_folders()

    # Mount all the USBs
    mount_all(mounted_usbs)

    return


if __name__ == "__main__":
    # Set up the program
    init_debug()
    init_main()
    init_gui("192.168.3.1", 8080)

    # Run the main program and catch the exit to stop the debug session
    try:
        main()
    finally:
        close_debug_session()
        gui_close()
