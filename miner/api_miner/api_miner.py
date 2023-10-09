import os
import argparse
import bittensor as bt
import requests

from miner.base_miner.base_miner import BaseMiner

class APIMiner(BaseMiner):

    def __init__(self, config):
        super().__init__(config)
        
        self.model_url = config.model.url
        self.model_name = config.model.name

        if self.model_name is None:
            raise ValueError(
                "Model name is None: the miner requires an model name an --model.name argument."
            )
        
        if self.model_url is None:
            raise ValueError(
                "Model URL is None: the miner requires an model api endpoint url as an --model.url argument."
            )
        
        self.prompt_format = {
            "prefix":"A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.",
            "assistant_start":'\nASSISTANT:',
            "assistant_end":'</s>',

            "user_start":'\nUSER: ',
            "user_end":'',
            }

    
    def generate(self, prompt, max_tokens = 1000, timeout=30):
      prompt = "<prefix><user_start>"+prompt+"<assistant_start>"
      prompt = self.replace_keywords(prompt)
      return self.generate_text(prompt, max_tokens=max_tokens, temperature=0.7, timeout=timeout)
    

    def replace_keywords(self,prompt):

        prompt = prompt.replace("<prefix>",self.prompt_format["prefix"])

        prompt = prompt.replace("<assistant_start>",self.prompt_format["assistant_start"])
        prompt = prompt.replace("<assistant_end>",self.prompt_format["assistant_end"])

        prompt = prompt.replace("<user_start>",self.prompt_format["user_start"])
        prompt = prompt.replace("<user_end>",self.prompt_format["user_end"])

        return prompt
    
    def generate_text(self, input_text, max_tokens=100, temperature = 0.0, timeout=30):
        return self.call_endpoint(input_text, max_tokens,temperature=temperature, timeout=timeout)[0]

    def call_endpoint(self, prompt, max_tokens, temperature, n=1, timeout=30):

        data = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "n":n,
            "stop":self.prompt_format["user_start"],
        }
        
        response = requests.post(self.model_url, headers={'Content-Type': 'application/json'}, json=data, timeout=timeout)
        generations = []
        if response.json().get("choices"):
            for d in response.json()["choices"]:
                generations.append(d["text"])

        return generations

def get_config():

    parser = argparse.ArgumentParser()

    parser.add_argument('--model.url', type=str, help='URL of the Miner API Endpoint')
    parser.add_argument('--model.name', type=str, help='Name of the Miner model to use')

    parser.add_argument(
        '--category', 
        type=str, 
        default = 'general_chat', 
        help = 'Category of the miner'
    )

    parser.add_argument( '--netuid', type = int, default = 1, help = "The chain subnet uid." )
    
    # Adds subtensor specific arguments i.e. --subtensor.chain_endpoint ... --subtensor.network ...
    bt.subtensor.add_args(parser)
    
    # Adds logging specific arguments i.e. --logging.debug ..., --logging.trace .. or --logging.logging_dir ...
    bt.logging.add_args(parser)
    
    # Adds wallet specific arguments i.e. --wallet.name ..., --wallet.hotkey ./. or --wallet.path ...
    bt.wallet.add_args(parser)
    
    # Adds axon specific arguments i.e. --axon.port ...
    bt.axon.add_args(parser)

    # To print help message, run python3 template/miner.py --help
    config = bt.config(parser)

    # Set up logging directory
    config.full_path = os.path.expanduser(
        "{}/{}/{}/netuid{}/{}".format(
            config.logging.logging_dir,
            config.wallet.name,
            config.wallet.hotkey,
            config.netuid,
            'miner',
        )
    )

    if not os.path.exists(config.full_path): os.makedirs(config.full_path, exist_ok=True)
    return config


# Main takes the config and starts the miner.
def main( config ):
    miner_model = APIMiner(config=config)
    miner_model.forward()

# This is the main function, which runs the miner.
if __name__ == "__main__":
    main( get_config() )