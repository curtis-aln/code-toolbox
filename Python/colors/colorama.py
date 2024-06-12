from colorama import init, Fore, Style

init()  # initialize colorama

color_map = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
}

def get_with_color(text, color="white"):
    """
    Prints the given text in the specified color using colorama.
    
    Arguments:
    - text (str): The text to print.
    - color (str): The color to print the text in. Defaults to "white".
                   Must be one of: "black", "red", "green", "yellow",
                   "blue", "magenta", "cyan", "white".
    """
    
    if color.lower() in color_map:
        return color_map[color.lower()] + text + Style.RESET_ALL
    else:
        return text
