import os
import sys

from PythonTools.debug import debug_message, init_debug, close_debug_session, handle_arg
from PythonTools.files import UserData
from PythonTools.network import get_ip
from PythonTools.renderer import Menu, clear, render_text, get_input, init_gui, gui_close
from PythonTools.tools import string_bool, ip_address
from USB import detect_usbs, unmount_all, mount_all, clean_folders, unmount_usb, mount_usb, check_mounted


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
        clean_folders()
        mounted_usbs = detect_usbs()

        # Add them after the refresh button
        for usb in mounted_usbs:
            item_names.append(f"{usb[0]} | {usb[1]}")
            if check_mounted(usb):
                item_values.append('<i class="fa-solid fa-eject" style="font-size: 24px"></i>')
            else:
                item_values.append('Click To Mount')

        menu_items = [item_names, item_values]
        main_menu = Menu(f"SAMBA Server: 192.168.3.1/RaspberryPI", menu_items, True)
        main_menu.time_limit = 1
        user_input = main_menu.get_input()

        # Check if the user refreshed the USBs or closed the server
        match user_input:
            case "Refresh USBs":
                debug_message("-= Refreshing Usbs... =-")
                continue

            case "Close Server":
                debug_message("-= Closing server... =-")
                break

        # User must have selected a USB

        # Find the USB
        if user_input is not None:
         for usb in mounted_usbs:

            # Check if the device name is in the user input
            if usb[0] in user_input:

                # If it is not mounted then mount the usb
                if not check_mounted(usb):
                   debug_message("-= Mounting USB... =-")
                   mount_usb(usb)
                else:
                   debug_message("-= Unmounting USB... =-")
                   unmount_usb(usb)
                break
    # Once the server has closed write a message
    closed_menu = Menu("Server Closed", [])
    debug_message("Replaced main screen with closed screen")
    closed_menu.show_menu()

    # Stop the SMB server
    os.system("sudo systemctl stop smbd")
    debug_message("Stopped SMB server")


def init_main() -> None:
    # Make sure the server folder is not delted
    os.system("sudo touch /External/.server")

    # Start the SMB server
    os.system("sudo systemctl start smbd")

    # Create the program folder if it doesnt exist
    if not os.path.exists("ProgramData"):
      os.mkdir("ProgramData")

    # Detect the USBs
    mounted_usbs = detect_usbs()

    # Un Mount any old USBs
    unmount_all(mounted_usbs)

    # Clean the External folder
    clean_folders()

    # Refresh the USBs
    mmounted_usbs = detect_usbs()

    # Mount all the USBs
    mount_all(mounted_usbs)

    # Log that the init is done
    debug_message("-= Server Init Done =-")

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
