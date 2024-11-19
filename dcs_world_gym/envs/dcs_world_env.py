from abc import abstractmethod
import gymnasium as gym
import numpy as np
import socket, time, re, json

from gymnasium import spaces
from .dcs_command import DCSCommand, parse_command

from geopy import distance 


class BaseEnvClient(gym.Env):
    
    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def reset(self):
        pass

class DcsWorldBaseClient(BaseEnvClient):

    reset_command = {DCSCommand.RESTART_MISSION: True}
    pause_command = {DCSCommand.PAUSE: True}

    def __init__(
            self,
            port: int,
            **kwargs,
        ):
        self.port = port

        self.max_step_length = kwargs.pop('max_step_length', 2048)
        self.cur_step = 0
        self.is_task_initialized = False

        self.initialize_socket() 

        self.connection = None
        
    def initialize_socket(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', self.port))
        self.sock.listen(1)
        print(f"Server is listening on port {self.port}...")


    def establish_connection(self):
        connection, client_address = self.sock.accept()
        print(f"Connection established with {client_address}")
        self.connection = connection

    def _post(self, command):
        try:
            _ = self.connection.sendall(command.encode())
        except Exception as e:
            print(f"Error in sending control message: {e}")
        return       

    def _request_env_message(self):
        message = None
        while not message:
            data = self.connection.recv(8192)
            message = data.decode('utf-8')

        message = message.split('\n\n')

        if len(message) > 2:
            print(f'Warning: get more than one observations.')
            print(message)
        return message[0]
        

    def _post_and_receive(self, message):
        command = parse_command(message)
        while True:
            try:
                self._post(command)
                response = self._request_env_message()
                return response
            except socket.timeout:
                print("Error: time out")
                pass
            except Exception as e:
                print(f"Error: {e}")

    def _parse_env_message(self, message):
        """
            The environment returns with rich information about the relative time in DCS world and the flight status of aircrafts, including self, which is the player controlled aircraft, and others, which is indexd by UNIT_ID. All info are arranged in json format.
            # For player controlled aircraft
            {
                'system':
                {
                    'time': relative time in DCS world, started from 0.
                },
                'self':
                {
                    'name': model of aircraft,
                    'country': allies or enemy,
                    'LatLongAlt': a 3d vector describing the abosulate position, please use tools such as geopy to convert it to relative positions in meters or kilometers,
                    'Attitude': a 3d vector [roll, pitch, yaw] in radius,
                    'Velocity': a 3d vector describing velocities along each axis, [north, upwards, east],
                    'AngularVelocity': a 3d vector describing angular velocity, [roll, yaw, pitch],
                    'Heading': heading direction, the same as yaw (Attitude[2]),
                    'TAS': True speed, the same as the |Velocity|
                },
                'UNIT_ID':
                {
                    'name': model of aircraft,
                    'unit': name of this unit, created within DCS mission editor,
                    'country': allies or enemy,
                    'LatLongAlt': a 3d vector describing the abosulate position, please use tools such as geopy to convert it to relative positions in meters or kilometers,
                    'Attitude': a 3d vector [roll, pitch, yaw] in radius
                }
            }
        """
        raise NotImplementedError

    def _parse_action(self, action):
        raise NotImplementedError
    
    def _get_reward(self, obs):
        """
            Task function
        """
        raise NotImplementedError

    def _check_terminated(self, message=None):
        """
            Task function
        """
        raise NotImplementedError

    def _check_truncated(self, message=None):
        if self.max_step_length:
            return self.cur_step >= self.max_step_length
        else:
            return False

    def step(self, action):

        if not self.is_task_initialized:
            raise AssertionError("Task has not be initialzed yet. Run 'self.reset()' first to initialize task.")
        self.cur_step += 1
        action_command = self._parse_action(action)
        message = self._post_and_receive(action_command)
        terminated = self._check_terminated(message)      
        truncated = self._check_truncated(message)

        if terminated or truncated:
            self.is_task_initialized = False
            obs = self.obs
            reward = self.reward
        else:
            self.obs = obs = self._parse_env_message(message)
            self.reward = reward = self._get_reward(obs)

        info = {
            "message": message
        }        

        return obs, reward, terminated, truncated, info


    def reset(self, **kwargs):

        if self.connection:
            _ = self._post_and_receive(self.reset_command)
            self.connection.close()
            self.connection = None

        self.establish_connection()

        message = self._request_env_message()

        print(f'Receive mesage: {message}.')

        message = self._post_and_receive(self.pause_command)

        self.cur_step = 0
        self.is_task_initialized = True
        self.obs = obs = self._parse_env_message(message)
        self.reward = -np.inf

        info = {
            "message": message,
        }
        return obs, info

    def close(self):
        self.connection.close()
    
    def _coordinate(self,pt):
        x = distance.distance(pt[:2], [0,pt[1]]).km
        y = distance.distance(pt[:2], [pt[0],0]).km
        h=pt[2]/1000
        return [x,y,h]



'''
class DcsWorldEmptyEnv(DcsWorldBaseClient):

    observation_space = spaces.Box(-np.inf, np.inf, shape = (13,))
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
        heading = data['self']['Heading']

        return np.array(latlongalt + attitude + velocity + angular_velocity + [heading] )
    

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
    
    




class DcsWorldEasyUTurnWithDiscreteAction(DcsWorldBaseClient):

    observation_space = spaces.Box(-np.inf, np.inf, shape = (13,))
    action_space = spaces.Discrete(4)

    target_heading = 0
    target_height = 2.43543859

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
        heading = data['self']['Heading']

        return np.array(latlongalt + attitude + velocity + angular_velocity + [heading] )
    

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
        cur_heading, cur_pitch, cur_height = obs[-1], obs[0], obs[6]
        # print(obs)
        heading_reward = np.cos(cur_heading - self.target_heading) + 1
        height_penalty = np.abs(cur_height - self.target_height) 
        pitch_penalty =  np.abs(cur_pitch) / np.pi
        if pitch_penalty < 0.25:
            pitch_penalty = 0
        return heading_reward - 0.1 * height_penalty - pitch_penalty

    def _check_terminated(self, message):
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError as e:
            print(message)
            raise json.decoder.JSONDecodeError

        return 'self' not in data.keys()
'''