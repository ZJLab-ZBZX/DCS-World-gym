import gymnasium as gym
import numpy as np

import stable_baselines3 as sb3
from stable_baselines3.common.vec_env import VecNormalize, DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy


from dcs_world_gym import DcsWorldTurnEnv, DcsWorldTurnWithDiscreteAction

### Load env
env = lambda: DcsWorldTurnEnv(
    port = 10010,
)
env = DummyVecEnv([env])
env_path = '/home/dcs/workspace/runs/2qv4yts4/checkpoints/model_vecnormalize_100000_steps.pkl'
env = VecNormalize.load(env_path, env)
env.training = False
env.norm_reward = False

### Load model
model_path = '/home/dcs/workspace/runs/2qv4yts4/checkpoints/model_100000_steps.zip'
model = sb3.PPO.load(model_path)


### Evaluate model
mean_reward, std_reward = evaluate_policy(model.policy, env, n_eval_episodes=10, deterministic=True)

print(f"mean_reward={mean_reward:.2f} +/- {std_reward}")



