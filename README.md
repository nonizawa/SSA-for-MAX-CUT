# SSA-for-MAX-CUT

[![GitHub license](https://img.shields.io/github/license/nonizawa/SSA-for-MAX-CUT)](https://github.com/nonizawa/SSA-for-MAX-CUT/blob/main/LICENSE)

Under construction...

SSA-for-MAX-CUT is an implementation of the Simulated Simultaneous Annealing algorithm for solving the MAX-CUT problem. This repository contains code that can be used to experiment with this optimization algorithm based on the research in the papers ["Fast-Converging Simulated Annealing for Ising Models Based on Integral Stochastic Computing"](https://ieeexplore.ieee.org/document/9743572) ["Local Energy Distribution Based Hyperparameter Determination for Stochastic Simulated Annealing"](https://arxiv.org/abs/2304.11839) by [N. Onizawa, et al.,].

## Table of Contents
1. [Background](#background)
2. [Installation](#installation)
3. [Usage](#usage)
4. [License](#license)
5. [Citation](#citation)
6. [Contributing](#contributing)

## Background

The MAX-CUT problem is a well-known problem in combinatorial optimization. This repository contains an implementation of the Stochastic Simulated Annealing (SSA) algorithm to tackle the MAX-CUT problem as described in the research paper ["Fast-Converging Simulated Annealing for Ising Models Based on Integral Stochastic Computing"](https://ieeexplore.ieee.org/document/9743572).

## Installation

### Prerequisites

- Python 3.x
- [Other dependencies and libraries]

### Clone the Repository

To get started, clone the repository using git:

```sh
git clone https://github.com/nonizawa/SSA-for-MAX-CUT.git
cd SSA-for-MAX-CUT
```

## Usage

### Single Run
To run the Simulated Simultaneous Annealing (SSA) algorithm on a single instance, use the sa.py script. For example:

```sh
python3 sa.py [options]
```
[Explain the options and arguments if necessary]

### Batch Processing
To run the Simulated Simultaneous Annealing (SSA) algorithm on multiple instances in a batch, use the batch_sa.sh script. For example:

```sh
./batch_sa.sh
```
[Explain any customization or configurations if necessary]

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
Here is the following paper describing hyperparameters for SSQA:
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