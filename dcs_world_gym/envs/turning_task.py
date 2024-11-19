import numpy as np
import json

from gymnasium import spaces
from .dcs_command import DCSCommand
from .dcs_world_env import DcsWorldBaseClient

class DcsWorldTurnEnv(DcsWorldBaseClient):

    observation_space = spaces.Box(-np.inf, np.inf, shape = (12,))
    action_space = spaces.Box(-1, 1, shape = (3,))

    target_heading = 0

    def _parse_env_message(self, message):
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError as e:
            print(message)
            raise json.decoder.JSONDecodeError
        

        latlongalt = self._coordinate(data['self']['LatLongAlt'] )
        attitude = data['self']['Attitude']
        velocity = data['self']['Velocity']
        angular_velocity = data['self']['AngularVelocity']
        # heading = data['self']['Heading']

        return np.array(latlongalt + attitude + velocity + angular_velocity)
    

    def _parse_action(self, action):
        pitch, roll, rudder = action
        command = {
            DCSCommand.PITCH: pitch,
            DCSCommand.ROLL: roll,
            DCSCommand.RUDDER: rudder,
        }
        return command

    def _get_reward(self, obs):
        cur_heading = obs[-1]
        return np.cos(cur_heading - self.target_heading) + 1

    def _check_terminated(self, message):
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError as e:
            print(message)
            raise json.decoder.JSONDecodeError

        return 'self' not in data.keys()
    
    




class DcsWorldTurnWithDiscreteAction(DcsWorldBaseClient):

    observation_space = spaces.Box(-np.inf, np.inf, shape = (12,))
    action_space = spaces.Discrete(4)

    target_heading = 0

    def _parse_env_message(self, message):
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError as e:
            print(message)
            raise json.decoder.JSONDecodeError
        

        latlongalt = self._coordinate(data['self']['LatLongAlt'] )
        attitude = data['self']['Attitude']
        velocity = data['self']['Velocity']
        angular_velocity = data['self']['AngularVelocity']
        # heading = data['self']['Heading']

        return np.array(latlongalt + attitude + velocity + angular_velocity)
    

    def _parse_action(self, action):
        if action == 0:
            command = {
                DCSCommand.UPSTART: True,
                DCSCommand.DOWNSTOP: True,
                DCSCommand.LEFTSTOP: True,
                DCSCommand.RIGHTSTOP: True,
            }
        elif action == 1:
            command = {
                DCSCommand.UPSTOP: True,
                DCSCommand.DOWNSTART: True,
                DCSCommand.LEFTSTOP: True,
                DCSCommand.RIGHTSTOP: True,
            }
        elif action == 2:
            command = {
                DCSCommand.UPSTOP: True,
                DCSCommand.DOWNSTOP: True,
                DCSCommand.LEFTSTART: True,
                DCSCommand.RIGHTSTOP: True,
            }
        elif action == 3:
            command = {
                DCSCommand.UPSTOP: True,
                DCSCommand.DOWNSTOP: True,
                DCSCommand.LEFTSTOP: True,
                DCSCommand.RIGHTSTART: True,
            }
        return command

    def _get_reward(self, obs):
        cur_heading = obs[-1]
        return np.cos(cur_heading - self.target_heading) + 1
    
    def _check_terminated(self, message):
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError as e:
            print(message)
            raise json.decoder.JSONDecodeError

        return 'self' not in data.keys()