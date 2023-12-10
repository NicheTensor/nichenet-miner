import typing
import bittensor as bt

class PromptingProtocol( bt.Synapse ):

    # Required request input, filled by sending dendrite caller.
    prompt_input: dict

    # Optional request output, filled by recieving axon.
    prompt_output: typing.Optional[dict] = None

    def deserialize(self) -> dict:
        """
        Deserialize the prompt output. This method retrieves the response from
        the miner in the form of prompt_output, deserializes it and returns it
        as the output of the dendrite.query() call.

        Returns:
        - dict: The deserialized response, which in this case is the value of prompt_output.
        """

        return self.prompt_output