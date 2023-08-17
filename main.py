import os
import sys

from lib.external.Maxs_Modules.debug import debug_message, init_debug, close_debug_session, handle_arg
from lib.external.Maxs_Modules.files import UserData
from lib.external.Maxs_Modules.game import get_saved_games, Game
from lib.external.Maxs_Modules.network import get_ip
from lib.external.Maxs_Modules.renderer import Menu, clear, render_text, get_input, init_gui, gui_close
from lib.external.Maxs_Modules.tools import string_bool, ip_address


def getUSBs():
    return [["asd", "asd"]]


def main() -> None:
    """
    The main function, initialise the program and show the main menu
    """

    # Loop until stopped
    while True:
        menu_items = [["Refresh USBs", "_Refresh Button"], getUSBs(), ["Eject USB", "_Eject Button"], ["Close Server", "_Quit Button"]]
        render_text(menu_items)


def init_main() -> None:
    # Init stuff here
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