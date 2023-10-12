# OpenAI NichetNet Miner

This repository contains a NicheNet Miner that uses OpenAI's GPT-3.5-turbo model as its synapse. The miner connects to the NicheNet Bittensor network, registers its wallet, and serves the GPT-3.5-turbo model to the network by attaching the prompt function to the axon.

## Prerequisites

- Python 3.8+
- OpenAI Python API (https://github.com/openai/openai)

## Installation

1. Clone the repository
2. Install the required packages with `pip install -r requirements.txt`
3. Ensure that you have your OpenAI key in your os environment variable
```bash
# Sets your openai key in os envs variable
export OPENAI_API_KEY='your_openai_key_here'

# Verifies if openai key is set correctly
echo $OPENAI_API_KEY
```

For more configuration options related to the wallet, axon, subtensor, logging, and metagraph, please refer to the Bittensor documentation.

## Example Usage

To run the OpenAI NicheNet Bittensor Miner with default settings, use the following command:

```
python3 -m pip install -r requirements.txt 

export OPENAI_API_KEY='sk-yourkey'

python -m miner.openai_miner.openai_miner 
    --netuid <your netuid>  # Must be attained by following the instructions in the docs/running_on_*.md files
    --subtensor.chain_endpoint <your chain url>  # Must be attained by following the instructions in the docs/running_on_*.md files
    --wallet.name <your miner wallet> # Must be created using the bittensor-cli
    --wallet.hotkey <your validator hotkey> # Must be created using the bittensor-cli
    --logging.debug # Run in debug mode, alternatively --logging.trace for trace mode
    --openai.api_key <your openai key> # OpenAI key
```