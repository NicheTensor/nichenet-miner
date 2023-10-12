# APIMiner NichetNet

This repository contains a NicheNet Miner that uses Miner deployed on some endpoint as its synapse. The miner connects to the NicheNet Bittensor network, registers its wallet, and serves the Miner deployed on an api endpoint to the network by attaching the prompt function to the axon.

## Prerequisites

- Python 3.8+

## Installation

1. Clone the repository
2. Install the required packages with `pip install -r requirements.txt`

For more configuration options related to the wallet, axon, subtensor, logging, and metagraph, please refer to the Bittensor documentation.

## Example Usage

To run the APIMiner with default settings, use the following command:

```
python3 -m pip install -r requirements.txt 

python -m miner.api_miner.api_miner 
    --netuid <your netuid>  # Must be attained by following the instructions in the docs/running_on_*.md files
    --subtensor.chain_endpoint <your chain url>  # Must be attained by following the instructions in the docs/running_on_*.md files
    --wallet.name <your miner wallet> # Must be created using the bittensor-cli
    --wallet.hotkey <your validator hotkey> # Must be created using the bittensor-cli
    --logging.debug # Run in debug mode, alternatively --logging.trace for trace mode
    --model.name <model name> # The name of deployed miner model
    --model.url <model url> # The api endpoint url for miner model
```