import gymnasium as gym
import numpy as np
import os

import stable_baselines3 as sb3
from stable_baselines3.common.callbacks import CallbackList, CheckpointCallback, EvalCallback
from stable_baselines3.common.vec_env import VecNormalize, DummyVecEnv
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env


import wandb
from wandb.integration.sb3 import WandbCallback

from dcs_world_gym import DcsWorldTurnEnv, DcsWorldTurnWithDiscreteAction



### Wandb init
config = {
    "policy_type": "MlpPolicy",
    "total_timesteps": 1e5,
    "env_name": "DCS_turning",
}

run = wandb.init(
    project = 'dcs_world_turning_task',
    config = config,
    sync_tensorboard = True,
    monitor_gym = False,
    save_code=True
)


### env init

env = DcsWorldTurnEnv(
    port = 10010, ### the same as Export.lua file
)
env = Monitor(env)

env = VecNormalize(DummyVecEnv( [lambda: env] ))


wandb_callback = WandbCallback(
    gradient_save_freq=1e4,
    model_save_path=f"models/{run.id}",
    verbose=2,
)

checkpoint_callback = CheckpointCallback(
    save_freq = 1e4,
    save_path = f'./runs/{run.id}/checkpoints/',
    name_prefix = 'model',
    save_replay_buffer=True,
    save_vecnormalize=True,
)


callback = CallbackList([wandb_callback, checkpoint_callback])

### model init
policy_kwargs = {
    "share_features_extractor": False,
    "optimizer_kwargs":{
        "eps": 1e-7,
        "betas": (0.9, 0.999),
    }
}


model = sb3.PPO(
    'MlpPolicy', 
    env, 
    verbose = 1, 
    tensorboard_log=f"runs/{run.id}",
    policy_kwargs= policy_kwargs,
    learning_rate = lambda f: f * 3e-4,
    # n_steps = 2048,
)


### learning
model.learn(
    total_timesteps=int(1e6), 
    callback=callback,
    progress_bar=True,
)


### saving model and env stats
log_dir = 'models/simple_turn'
model.save( os.path.join(log_dir, "ppo") )
env.save( os.path.join(log_dir, "env.pkl"))