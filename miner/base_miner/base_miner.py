import bittensor as bt
import template
import time
import traceback
import typing

class BaseMiner:

    def __init__(self, config):

        self.config = config

        # Activating Bittensor's logging with the set configurations.
        bt.logging(config=config, logging_dir=config.full_path)

        bt.logging.info(config)

        # Wallet holds cryptographic information, ensuring secure transactions and communication.
        self.wallet = bt.wallet( config = config )
        bt.logging.info(f"Wallet: {self.wallet}")

        # subtensor manages the blockchain connection, facilitating interaction with the Bittensor blockchain.
        self.subtensor = bt.subtensor( config = config )
        bt.logging.info(f"Subtensor: {self.subtensor}")

        # metagraph provides the network's current state, holding state about other participants in a subnet.
        self.metagraph = self.subtensor.metagraph(config.netuid)
        bt.logging.info(f"Metagraph: {self.metagraph}")

        if self.wallet.hotkey.ss58_address not in self.metagraph.hotkeys:
            bt.logging.error(f"\nYour validator: {self.wallet} if not registered to chain connection: {self.subtensor} \nRun btcli register and try again. ")
            exit()
        else:
            # Each miner gets a unique identity (UID) in the network for differentiation.
            self.my_subnet_uid = self.metagraph.hotkeys.index(self.wallet.hotkey.ss58_address)
            bt.logging.info(f"Running miner on uid: {self.my_subnet_uid}")

    # The following functions control the miner's response to incoming requests.
    # The blacklist function decides if a request should be ignored.
    def blacklist_fn(self, synapse: template.protocol.PromptingProtocol ) -> typing.Tuple[bool, str]:

        # TODO(developer): Define how miners should blacklist requests. This Function 
        # Runs before the synapse data has been deserialized (i.e. before synapse.data is available).
        # The synapse is instead contructed via the headers of the request. It is important to blacklist
        # requests before they are deserialized to avoid wasting resources on requests that will be ignored.
        # Below: Check that the hotkey is a registered entity in the metagraph.

        if synapse.dendrite.hotkey not in self.metagraph.hotkeys:
            # Ignore requests from unrecognized entities.
            bt.logging.trace(f'Blacklisting unrecognized hotkey {synapse.dendrite.hotkey}')
            return True, "Unrecognized hotkey"
        
        # TODO(developer): In practice it would be wise to blacklist requests from entities that 
        # are not validators, or do not have enough stake. This can be checked via metagraph.S
        # and metagraph.validator_permit. You can always attain the uid of the sender via a
        # metagraph.hotkeys.index( synapse.dendrite.hotkey ) call.
        # Otherwise, allow the request to be processed further.

        bt.logging.trace(f'Not Blacklisting recognized hotkey {synapse.dendrite.hotkey}')
        return False, "Hotkey recognized!"

    # The priority function determines the order in which requests are handled.
    # More valuable or higher-priority requests are processed before others.
    def priority_fn( self, synapse: template.protocol.PromptingProtocol ) -> float:

        # TODO(developer): Define how miners should prioritize requests.
        # Miners may recieve messages from multiple entities at once. This function
        # determines which request should be processed first. Higher values indicate
        # that the request should be processed first. Lower values indicate that the
        # request should be processed later.
        # Below: simple logic, prioritize requests from entities with more stake.

        caller_uid = self.metagraph.hotkeys.index( synapse.dendrite.hotkey ) # Get the caller index.
        prirority = float( self.metagraph.S[ caller_uid ] ) # Return the stake as the priority.
        bt.logging.trace(f'Prioritizing {synapse.dendrite.hotkey} with value: ', prirority)
        return prirority
    
        # This is the core miner function, which decides the miner's response to a valid, high-priority request.
    def prompting(self, synapse: template.protocol.PromptingProtocol ) -> template.protocol.PromptingProtocol:
        # TODO(developer): Define how miners should process requests.
        # This function runs after the synapse has been deserialized (i.e. after synapse.data is available).
        # This function runs after the blacklist and priority functions have been called.

        category = self.config.category
        tags = []

        # Return miner category when requested by validator
        get_miner_info = synapse.prompt_input['get_miner_info']
        if get_miner_info:
            synapse.prompt_output = {'category': category, 'tags': tags}
            return synapse

        question = synapse.prompt_input['prompt']
        max_tokens = synapse.prompt_input['max_tokens']
        max_response_time = synapse.prompt_input['max_response_time']

        reply = self.generate(question, max_tokens=max_tokens)
        synapse.prompt_output = {"response": reply, "category": category, "tags": tags}

        return synapse
    
    def generate(self):
        raise NotImplementedError("Method `generate` must be implemented in child classes of BaseMiner.")

    def forward(self):
        
        # Step 5: Build and link miner functions to the axon.
        # The axon handles request processing, allowing validators to send this process requests.
        self.axon = bt.axon( wallet = self.wallet, port = self.config.axon.port)
        bt.logging.info(f"Axon {self.axon}")

        # Attach determiners which functions are called when servicing a request.
        bt.logging.info(f"Attaching forward function to axon.")
        self.axon.attach(
            forward_fn = self.prompting,
            blacklist_fn = self.blacklist_fn,
            priority_fn = self.priority_fn,
        )

        # Serve passes the axon information to the network + netuid we are hosting on.
        # This will auto-update if the axon port of external ip have changed.
        bt.logging.info(f"Serving axon {self.prompting} on network: {self.config.subtensor.chain_endpoint} with netuid: {self.config.netuid}")
        self.axon.serve( netuid = self.config.netuid, subtensor = self.subtensor )

        # Start  starts the miner's axon, making it active on the network.
        bt.logging.info(f"Starting axon server on port: {self.axon.port}")
        self.axon.start()

        # Step 6: Keep the miner alive
        # This loop maintains the miner's operations until intentionally stopped.
        bt.logging.info(f"Starting miner loop.")
        step = 0
        while True:
            try:
                # TODO(developer): Define any additional operations to be performed by the miner.
                # Below: Periodically update our knowledge of the network graph.
                if step % 5 == 0:
                    self.metagraph = self.subtensor.metagraph(self.config.netuid)
                    log =  (f'Step:{step} | '\
                            f'Block:{self.metagraph.block.item()} | '\
                            f'Stake:{self.metagraph.S[self.my_subnet_uid]} | '\
                            f'Rank:{self.metagraph.R[self.my_subnet_uid]} | '\
                            f'Trust:{self.metagraph.T[self.my_subnet_uid]} | '\
                            f'Consensus:{self.metagraph.C[self.my_subnet_uid] } | '\
                            f'Incentive:{self.metagraph.I[self.my_subnet_uid]} | '\
                            f'Emission:{self.metagraph.E[self.my_subnet_uid]}')
                    bt.logging.info(log)
                step += 1
                time.sleep(1)

            # If someone intentionally stops the miner, it'll safely terminate operations.
            except KeyboardInterrupt:
                self.axon.stop()
                bt.logging.success('Miner killed by keyboard interrupt.')
                break
            # In case of unforeseen errors, the miner will log the error and continue operations.
            except Exception as e:
                bt.logging.error(traceback.format_exc())
                continue