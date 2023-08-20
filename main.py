import os
import sys

from PythonTools.debug import debug_message, init_debug, close_debug_session, handle_arg
from PythonTools.files import UserData
from PythonTools.network import get_ip
from PythonTools.renderer import Menu, clear, render_text, get_input, init_gui, gui_close
from PythonTools.tools import string_bool, ip_address
from USB import detect_usbs, unmount_all, mount_all, clean_folders


def main() -> None:
    """
    The main function, initialise the program and show the main menu
    """


    # Loop until stopped
    while True:
        item_names = ["Refresh USBs", "Close Server"]
        item_values = ["_Refresh Button", "_Quit Button"]

        # Detect the USBs
        mounted_usbs = detect_usbs()

        # Add them after the refresh button
        for usb in mounted_usbs:
            item_names.append(usb[0])
            item_values.append(f"MOUNTED: {usb[1]}")

        menu_items = [item_names, item_values]
        main_menu = Menu(get_ip(), menu_items, True)

        match main_menu.get_input():
            case _:
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
    init_gui()

    # Run the main program and catch the exit to stop the debug session
    try:
        main()
    finally:
        close_debug_session()
        gui_close()
