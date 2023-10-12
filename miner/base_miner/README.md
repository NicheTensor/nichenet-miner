# BaseMiner NichetNet

This repository contains the NicheNet BaseMiner class that is used to build NicheNet Miner. The miner connects to the NicheNet Bittensor network, registers its wallet, and serves the Miner deployed on an api endpoint to the network by attaching the prompt function to the axon.

## Prerequisites

- Python 3.8+

## Installation

1. Clone the repository
2. Install the required packages with `pip install -r requirements.txt`

For more configuration options related to the wallet, axon, subtensor, logging, and metagraph, please refer to the Bittensor documentation.

## Example Usage

To create Miner out of BaseMiner. See miner/api_miner/api_miner.py or miner/openai_miner/openai_miner.py    
Essentially you need to build `__init__` and `generate` function to create a miner.