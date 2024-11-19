# DCS-World-gym

** This repo is currently a work in progress and will be actively updating.** 

## Overview
A third party RL environment for DCS world, using the [gymnasium library](https://github.com/Farama-Foundation/Gymnasium). 

## Installation
1. Setup conda environment.
    ```
    $ conda create -n dcs_world python=3.11
    $ conda activate dcs_world
    ```

2. Clone this git repo to your local machine.
    ```
    $ git clone https://github.com/ZJLab-ZBZX/DCS-World-gym.git
    ```

3. Enter the repo root folder and install the package.
    ```
    $ pip install -r requirements.txt
    $ pip install -e .
    ```

4. Download and install [DCS world](https://www.digitalcombatsimulator.com/cn/downloads/world/), and modify game scripts following [DCS setup guide](./dcs_scripts).

## Example Usage

0. To test if the communication is setup correctly, run *comm_check.py* and start a mission in DCS World, you should be able to receive information about the game status.

1. Run the learning script with
    ```
    $ python demo_turning_task.py
    ```
    This will create a gym environment instance, listen to the specified port and wait until a mission begins. 

2. In DCS world, start a mission, e.g., *mission --> navi*.
3. To test a learned policy, run the script with
    ```
    $ python eval_model.py
    ```

## Acknowledgement
If you use this toolkit in your research, please cite it as follows:
```latex
@misc{ZJ2024DataProcessesToolkit,
 author = {Zhejiang Lab},
 title = {DCS-World-gym},
 year = {2024},
 howpublished = {\url{https://github.com/ZJLab-ZBZX/DCS-World-gym}},
 note = {Accessed: 2024-11-19}
}
```

## Contact us
If you have any issues or questions, feel free to contact us via email at cyzhao1991@gmail.com

© 2024 Research Center for Intelligent Equipment of Zhejiang Lab