# SSA-for-MAX-CUT (Stochastic simulated annealing for maximum cut problems)

[![GitHub license](https://img.shields.io/github/license/nonizawa/SSA-for-MAX-CUT)](https://github.com/nonizawa/SSA-for-MAX-CUT/blob/main/LICENSE)

SSA-for-MAX-CUT is an implementation of the stochastic simulated annealing (SSA) algorithm for solving the MAX-CUT problem. The MAX-CUT problem is a well-known problem in combinatorial optimization. This repository contains an implementation of the Stochastic Simulated Annealing (SSA) algorithm to tackle the MAX-CUT problem as described in the research paper ["Fast-Converging Simulated Annealing for Ising Models Based on Integral Stochastic Computing"](https://ieeexplore.ieee.org/document/9743572).　In addition, it contains an extented algorithm SSAU (SSA with unique noise magnitude) with the hyperparameter determintion in the research paper ["Local Energy Distribution Based Hyperparameter Determination for Stochastic Simulated Annealing"](https://arxiv.org/abs/2304.11839).


## Installation

### Prerequisites

- Python 3.x

### Install the required packages

```sh
pip install -r requirement.txt
```
Note that requirement.txt was generated using `pip freeze > requirement.txt`.

### Clone the Repository

To get started, clone the repository using git:

```sh
git clone https://github.com/nonizawa/SSA-for-MAX-CUT.git
cd SSA-for-MAX-CUT
```

## Structure


- `ssa.py`: This is the Python script that runs the SSA for MAX-CUT algorithm.
- `ssau.py`: This is the Python script that runs the SSAU for MAX-CUT algorithm.
- `sa.py`: This is the Python script that runs the SA for MAX-CUT algorithm.
- `utils.py`: This is the Python script that includes function for SSA and SSAU.
- `./graph/`: This directory contains the dataset of graphs used for evaluation.
- `./result/`: This directory contains the evaluation results generated using simulation.
- `batch_ssa.sh`: This is the shell script that runs the SSA for batch processing.
- `batch_ssau.sh`: This is the shell script that runs the SSAU for batch processing.
- `batch_sa.sh`: This is the shell script that runs the SA for batch processing.


## Single Run

### SSA (Stochastic simulated annealing)

To run the SSA algorithm on a single instance, use the sa.py script. For example:

```sh
python ssa.py --file_path graph/G1.txt --cylce 1000 --trial 100 --tau 1 --param 1
```
You can find the simulation results in ./result/.　Result***.csv includes simulation retsuls, such as mean cut values and simulation time. Cut***.csv includes cut values for all trials.

Here ia the options.

- `--file_path`: a graph file

- `--cycle`: Number of cycles for 1 trial

- `--trial`: Number of trials to evaluate the performance on average

- `--tau`:  A pseudo inverse temperature is increased every tau cycle

- `--param`: There are eight parameters written in ssa.py


### SSAU (Stochastic simulated annealing with unique noise magnitude)

Here is a python program for SSAU that can run, like SSA.
- `ssau.py`

It has the same options as well as SSA.


### SA (Traditional simulated annealing)

Also, here is a python program for traditional SA.
- `sa.py`

Here is the options.

--file-path: a graph file

- `--cycle`: Number of cycles for 1 trial

- `--trial`: Number of trials to evaluate the performance on average

- `--T_ini`:  Initial temperature

- `--T_min`: Minimum temperature (last temperature)

## Batch Processing

### SSA

To run the SSA algorithm on multiple graphs in a batch, use the batch_sa.sh script. For example:

```sh
./batch_ssa.sh
```
Before running, please modify line 17 to specify your Python path.

### SSAU

Here is a python program for SSAU.
- `batch_ssau.sh`

### SA

Also, here is a python program for traditional SA.
- `batch_sa.sh`

## Contact

For any questions, issues, or inquiries, feel free to create an issue in the repository or contact the repository owner [@nonizawa](https://github.com/nonizawa).

## Citation

If you use this code in your research, please cite the original paper:
```bibtex
@ARTICLE{9743572,
  author={Onizawa, Naoya and Katsuki, Kota and Shin, Duckgyu and Gross, Warren J. and Hanyu, Takahiro},
  journal={IEEE Transactions on Neural Networks and Learning Systems}, 
  title={Fast-Converging Simulated Annealing for Ising Models Based on Integral Stochastic Computing}, 
  year={2022},
  volume={},
  number={},
  pages={1-7},
  doi={10.1109/TNNLS.2022.3159713}}
```
Here is the following paper describing hyperparameters for SSA and SSAI:
```bibtex
@misc{onizawa2023local,
      title={Local Energy Distribution Based Hyperparameter Determination for Stochastic Simulated Annealing}, 
      author={Naoya Onizawa and Kyo Kuroki and Duckgyu Shin and Takahiro Hanyu},
      year={2023},
      eprint={2304.11839},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```

Here is a bibtex for the code.
```bibtex
@misc{nonizawa_SSAforMAXCUT,
	author = {Onizawa, Naoya},
	title = {{SSA-for-MAX-CUT}},
	year = {2023},
	journal = {GitHub Repository},
	url = {https://github.com/nonizawa/SSA-for-MAX-CUT}
	}
```

## License

This project is licensed under the MIT License.
