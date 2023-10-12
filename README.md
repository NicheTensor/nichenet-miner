# NicheNet
NicheNet is a network of specialized AI models, with abilities such as: storytelling, coding, scientific writing, and general chat.
The models on the network are continously measured and ranked, to ensure you can always get the best models available in any niche.
The network uses the Bittensor protocol, meaning it is open for anyone to participate with their model and get rewarded based on performance, ensuring that the latest and best models are always available.

# Introduction to Bittensor
The Bittensor blockchain hosts multiple self-contained incentive mechanisms 'subnets'. Subnets are playing fields through which miners (those producing value) and validators (those producing consensus) determine together the proper distribution of TAO for the purpose of incentivizing the creation of value, i.e. generating digital commodities, such as intelligence, or data. Each consists of a wire protocol through which miners and validators interact and their method of interacting with Bittensor's chain consensus engine [Yuma Consensus](https://bittensor.com/documentation/validating/yuma-consensus) which is designed to drive these actors into agreement about who is creating value.

# NichetNet Miner
This repository is a template for creating nichenet miners. The template is designed to be simple (rewards miners for responding with the multiple of the value sent by vaidators) and can act as a starting point for those who want to write their own mechanism.   
It is split into below primary files which you should rewrite:
- `template/protocol.py`: The file where the wire-protocol used by miners and validators is defined.   
- `miner/base_mine/base_miner.py`: This script which defines the base miner's behavior, i.e., how the miner responds to requests from validators.   
    -- `miner/api_miner/api_miner.py`: This script creates an API miner out of the base miner.   
    -- `miner/openai_miner/openai_miner.py`: This script creates an OpenAI Miner allowing models like gpt-3.5-turbo (chatgpt).   

---

# Running the template
Before running the template you will need to attain a subnetwork on either Bittensor's main network, test network, or your own staging network. To create subnetworks on each of these subnets follow the instructions in files below:
- `docs/running_on_staging.md`
- `docs/running_on_testnet.md`
- `docs/running_on_mainnet.md`

---

# Installation
This repository requires python3.8 or higher. To install, simply clone this repository and install the requirements.
```bash
git clone https://github.com/NicheTensor/nichenet-miner.git
cd nichenet-miner
python -m pip install -r requirements.txt
python -m pip install -e .
```
---

Once you have installed this repo and attained your subnet via the instructions in the nested docs (staging, testing, or main) you can run the miner with the following commands.
```bash
# To run the OpenAI Miner
python -m miner.openai_miner.openai_miner 
    --netuid <your netuid>  # Must be attained by following the instructions in the docs/running_on_*.md files
    --subtensor.chain_endpoint <your chain url>  # Must be attained by following the instructions in the docs/running_on_*.md files
    --wallet.name <your miner wallet> # Must be created using the bittensor-cli
    --wallet.hotkey <your validator hotkey> # Must be created using the bittensor-cli
    --logging.debug # Run in debug mode, alternatively --logging.trace for trace mode
    --openai.api_key <your openai key> # OpenAI key

# To run API Miner
python -m miner.api_miner.api_miner 
    --netuid <your netuid>  # Must be attained by following the instructions in the docs/running_on_*.md files
    --subtensor.chain_endpoint <your chain url>  # Must be attained by following the instructions in the docs/running_on_*.md files
    --wallet.name <your miner wallet> # Must be created using the bittensor-cli
    --wallet.hotkey <your validator hotkey> # Must be created using the bittensor-cli
    --logging.debug # Run in debug mode, alternatively --logging.trace for trace mode
    --model.name <model name> # The name of deployed miner model
    --model.url <model url> # The api endpoint url for miner model
```