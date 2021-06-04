from termcolor import colored
import json


def Debugging(text, color='yellow'):
    try:
        value = json.dumps(text, indent=4)
    except:
        value = text

    print(colored(value, color))