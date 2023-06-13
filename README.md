# SSA-for-MAX-CUT

[![GitHub license](https://img.shields.io/github/license/nonizawa/SSA-for-MAX-CUT)](https://github.com/nonizawa/SSA-for-MAX-CUT/blob/main/LICENSE)

SSA-for-MAX-CUT is an implementation of the Simulated Simultaneous Annealing algorithm for solving the MAX-CUT problem. This repository contains code that can be used to experiment with this optimization algorithm based on the research in the paper ["title-of-paper"](https://arxiv.org/abs/2304.11839) by [authors-name].

## Table of Contents
1. [Background](#background)
2. [Installation](#installation)
3. [Usage](#usage)
4. [License](#license)
5. [Citation](#citation)
6. [Contributing](#contributing)

## Background

The MAX-CUT problem is a well-known problem in combinatorial optimization. This repository contains an implementation of the Simulated Simultaneous Annealing (SSA) algorithm to tackle the MAX-CUT problem as described in the research paper ["title-of-paper"](https://arxiv.org/abs/2304.11839).

## Installation

### Prerequisites

- Python 3.x
- [Other dependencies and libraries]

### Clone the Repository

To get started, clone the repository using git:

```sh
git clone https://github.com/nonizawa/SSA-for-MAX-CUT.git
cd SSA-for-MAX-CUT

## Usage

### Single Run
To run the Simulated Simultaneous Annealing (SSA) algorithm on a single instance, use the sa.py script. For example:

sh
Copy code
python sa.py [options]
[Explain the options and arguments if necessary]

### Batch Processing
To run the Simulated Simultaneous Annealing (SSA) algorithm on multiple instances in a batch, use the batch_sa.sh script. For example:

sh
Copy code
./batch_sa.sh
[Explain any customization or configurations if necessary]

## License

This project is licensed under the MIT License.

## Citation

If you use this code in your research, please cite the original paper:
@misc{onizawa2023local,
      title={Local Energy Distribution Based Hyperparameter Determination for Stochastic Simulated Annealing}, 
      author={Naoya Onizawa and Kyo Kuroki and Duckgyu Shin and Takahiro Hanyu},
      year={2023},
      eprint={2304.11839},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}