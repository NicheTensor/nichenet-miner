import os
import argparse
import bittensor as bt
import openai
import time

from miner.base_miner.base_miner import BaseMiner

class OpenAIMiner(BaseMiner):
    def __init__(self, api_key, config):
        super().__init__(config)

        if not api_key:
            raise ValueError(
                "OpenAI API key is None: the miner requires an `OPENAI_API_KEY` defined in the environment variables or as an --openai.api_key argument."
            )
        
        openai.api_key = api_key

        if not self.is_api_key_valid():
            raise ValueError(
                "OpenAI API key is invalid: the miner requires a valid `OPENAI_API_KEY` defined in the environment variables or as an --openai.api_key argument."
            )

        self.model_name = config.model_name
        if self.model_name is None:
            self.model_name = 'gpt-3.5-turbo'

        self.system_prompt = config.openai.system_prompt
        if self.system_prompt is None:
            self.system_prompt = 'You are a helpful assistant.'

    def is_api_key_valid(self):
        try:
            _ = openai.Completion.create(
                engine="davinci",
                prompt="hey",
                max_tokens=5
            )
        except:
            return False
        else:
            return True

    def generate(self, question, max_tokens):

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": question},
        ]

        bt.logging.debug(f"messages: {messages}")
        bt.logging.debug(f"Model name: {self.model_name}")

        resp = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            max_tokens=max_tokens,
            # max_tokens=self.config.openai.max_tokens,
            temperature=self.config.openai.temperature,
            top_p=self.config.openai.top_p,
            frequency_penalty=self.config.openai.frequency_penalty,
            presence_penalty=self.config.openai.presence_penalty,
            n=self.config.openai.n,
        )["choices"][0]["message"]["content"]

        return resp

def get_config():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--openai.api_key",
        type=str,
        default=None,
        help="The OpenAI API key.",
    )

    parser.add_argument(
        "--openai.system_prompt",
        type=str,
        default=None,
        help="The system prompt.",
    )
    parser.add_argument(
        "--openai.max_tokens",
        type=int,
        default=100,
        help="The maximum number of tokens to generate in the completion.",
    )
    parser.add_argument(
        "--openai.temperature",
        type=float,
        default=0.4,
        help="Sampling temperature to use, between 0 and 2.",
    )
    parser.add_argument(
        "--openai.top_p",
        type=float,
        default=1,
        help="Nucleus sampling parameter, top_p probability mass.",
    )
    parser.add_argument(
        "--openai.n",
        type=int,
        default=1,
        help="How many completions to generate for each prompt.",
    )
    parser.add_argument(
        "--openai.presence_penalty",
        type=float,
        default=0.1,
        help="Penalty for tokens based on their presence in the text so far.",
    )
    parser.add_argument(
        "--openai.frequency_penalty",
        type=float,
        default=0.1,
        help="Penalty for tokens based on their frequency in the text so far.",
    )
    parser.add_argument(
        "--openai.model_name",
        type=str,
        default="gpt-3.5-turbo",
        help="OpenAI model to use for completion.",
    )

    # Common Args for all miners
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

    api_key = config.openai.api_key
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY", None)

    miner_model = OpenAIMiner(api_key=api_key, config=config)
    miner_model.forward()

# This is the main function, which runs the miner.
if __name__ == "__main__":
    main( get_config() )