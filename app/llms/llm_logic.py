# generic interface for the llm logic

from abc import ABC
from contextlib import AbstractContextManager


class LLMLogic(AbstractContextManager["LLMLogic"], ABC):
    """
    Abstract implementation of the client that is responsible for the logic of the LLM.
    """

    async def chat(self, prompt: str) -> str:
        """
        Chat with the model
        :param prompt: prompt to chat with the model
        :return: the output of the model
        """
        raise NotImplementedError("chat method must be implemented")
