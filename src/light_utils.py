import RPi.GPIO as gpio
import datetime as dt

from src import err 
from src import const


def switchLight(name, state):
    """
    Will switch the light on or off.

    Inputs:
        * name => <str> The name of the light (from the gpioPins dict in src.const)
        * state => <str | bool> 'on' or 'off' or True or False
    """
    # Check input types and things
    if isinstance(state, str):
        state = state.lower()
        if not any(state == j for j in ('on', 'off')):
            msg = "Sorry wrong input for the state in the switchLight"
            msg += " function.\nPlease enter:\n\t* 'on'\n\t* 'off'"
            raise SystemExit(msg)
        if state == 'on':
            state = False
        else:
            state = True
    elif isinstance(state, bool):
        state = not state  # So true is on and false is off
    else:
        msg = "Sorry wrong input for the state in the switchLight"
        msg += " function.\nPlease enter:\n\t* 'on'\n\t* 'off'"
        raise SystemExit(msg)

    if name not in const.gpioPins:
        msg = "`%s` is not in the gpioPins dictionary. Correct names are:" % name
        msg += "\n\t*" + "\n\t*".join(const.gpioPins)
        raise SystemExit(msg)

    # Now actually switch the lights
    pin = const.gpioPins[name]
    if gpio.input(pin) is not state:
        gpio.output(pin, state)

