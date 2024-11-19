from dataclasses import dataclass

@dataclass
class DCSCommand:

    NULL = 1

    ### Continuous Actions
    PITCH = 2001
    ROLL = 2002
    RUDDER = 2003
    THRUST = 2004
    DELTA_PITCH = 2013
    DELTA_ROLL = 2014
    DELTA_RUDDER = 2015
    DELTA_THRUST = 2016

    ### Discrete Actions
    RESET = 327
    RESTART_MISSION = 1641
    PAUSE = 52
    EJECT = 83
    DOWN = 186
    UP = 187
    LEFT = 188
    RIGHT = 189

    UPSTART = 193
    UPSTOP = 194
    DOWNSTART = 195
    DOWNSTOP = 196
    LEFTSTART = 197
    LEFTSTOP = 198
    RIGHTSTART = 199
    RIGHTSTOP = 200



def parse_command(command_dict):
    """
        Parse input action command dictionary to lua format.

        An example for input action format:
        {
            2001: 0.0,
            2002: 0.0,
            327: Ture,
            ......
        }
    """
    
    action_string_list = []
    for k, v in command_dict.items():
        if isinstance(v, bool):
            v = 'true' if v else 'false'
        action_string_list.append( f"[{k}]= {v}" )

    action_string = ', '.join(action_string_list)
    return '{' + action_string + '}\n'

