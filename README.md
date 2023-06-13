# SSA-for-MAX-CUT (Stochastic simulated annealing for maximum cut problems)

[![GitHub license](https://img.shields.io/github/license/nonizawa/SSA-for-MAX-CUT)](https://github.com/nonizawa/SSA-for-MAX-CUT/blob/main/LICENSE)

Under construction...

SSA-for-MAX-CUT is an implementation of the Simulated Simultaneous Annealing algorithm for solving the MAX-CUT problem. The MAX-CUT problem is a well-known problem in combinatorial optimization. This repository contains an implementation of the Stochastic Simulated Annealing (SSA) algorithm to tackle the MAX-CUT problem as described in the research paper ["Fast-Converging Simulated Annealing for Ising Models Based on Integral Stochastic Computing"](https://ieeexplore.ieee.org/document/9743572).　In addition, it contains an extented algorithm SSAI (SSA with individual noise) with the hyperparameter determintion in the research paper ["Local Energy Distribution Based Hyperparameter Determination for Stochastic Simulated Annealing"](https://arxiv.org/abs/2304.11839).


## Table of Contents
1. [Installation](#installation)
2. [Single run](#single)
3. [Batch processing](#batch)
4. [License](#license)
5. [Citation](#citation)



## Installation

### Prerequisites

- Python 3.x

### Clone the Repository

To get started, clone the repository using git:

```sh
git clone https://github.com/nonizawa/SSA-for-MAX-CUT.git
cd SSA-for-MAX-CUT
```

## Single Run

### SSA

To run the SSA algorithm on a single instance, use the sa.py script. For example:

```sh
python ssa.py --file_path graph/G1.txt --cylce 1000 --trial 100 --tau 1 --param 1
```
You can find the simulation results in ./result/.

Here ia the options.

--file_path: a graph file

--cycle: Number of cycles for 1 trial

--trial: Number of trials to evaluate the performance on average

--tau:  A pseudo inverse temperature is increased every tau cycle

--param: There are eight parameters written in ssa.py


### SSAI

Here is a python program for SSAI that can run, like SSA.
- ssai.py

It has the same options as well as SSA.


### SA

Also, here is a python program for traditional SA.
- sa.py

Here is the options.

--file-path: a graph file

--cycle: Number of cycles for 1 trial

--trial: Number of trials to evaluate the performance on average

--T_ini  Initial temperature

--T_min: Minimum temperature (last temperature)

## Batch Processing

### SSA

To run the SSA algorithm on multiple graphs in a batch, use the batch_sa.sh script. For example:

```sh
./batch_ssa.sh
```
Before running, please modify line 17 to specify your Python path.

### SSAI

Here is a python program for SSAI.
- batch_ssai.sh

### SA

Also, here is a python program for traditional SA.
- batch_sa.sh

## License

This project is licensed under the MIT License.

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
    author = {Naoya Onizawa,
    title = {SSA-for-MAX-CUT},
    year = {2023},
    publisher = {GitHub},
    journal = {GitHub Repository},
    howpublished = {\url{https://github.com/nonizawa/SSA-for-MAX-CUT}}
}
```