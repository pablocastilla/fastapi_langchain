from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import (
    SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
)
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import Any
from app.llms import Illm
from app.llms.token_cost_process import CostCalcAsyncHandler, TokenCostProcess
from langchain.memory import ConversationBufferMemory
import json
from app.queue_management.iqueue_management_system import IQueueManagementSystem


# Desired output format.
class EmergencyRoomTriage(BaseModel):
    name: str = Field(description="patient name")
    medical_specialty: str = Field(description="specialty to which the patient should be referred.In English.")
    urgency: int = Field(
        description="urgency level of the patient, 1 is the most urgent, 5 is the least urgent.In English.")
    response_to_the_user: str = Field(
        description="go to the waiting room if urgency level is above 1, go to emergency room if urgency level is 1.Use the language of the user.")


parser = PydanticOutputParser(pydantic_object=EmergencyRoomTriage)  # type: ignore

# system message prompt. It defines the instructions for the system.
template: str = """

            Previous conversation:
            {chat_history}

            You are a doctor in an emergency room doing the triage.Be very concise.

            Interfact with the user until you have the name.

            After that interact with the user until you have one description of the symptons.

            When you have the name and the symptons decide the specialty and the function and answer following this format:
            {format_instructions}

            """

system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

memory = ConversationBufferMemory(return_messages=True, input_key="text", memory_key="chat_history")


class OpenAILLMLogic(Illm.ILLM):
    """
    Implementation of the client that is responsible for the logic of the LLM.
    """

    def __init__(self, queue_management_system: IQueueManagementSystem) -> None:
        self.queue_management_system: IQueueManagementSystem = queue_management_system

    def __enter__(self) -> "OpenAILLMLogic":
        self.token_cost_process = TokenCostProcess()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        print(self.token_cost_process.get_cost_summary("gpt-3.5-turbo"))

    async def chat(self, prompt: str) -> str:
        """chat with the LLM."""

        llm = ChatOpenAI(temperature=0, callbacks=[CostCalcAsyncHandler("gpt-3.5-turbo", self.token_cost_process)])

        chain = LLMChain(llm=llm, prompt=chat_prompt, memory=memory, verbose=True)

        result: str = await chain.arun({'text': prompt, 'format_instructions': parser.get_format_instructions()})

        if self.is_json_convertible(result):
            json_result = json.loads(result)
            result = json_result['response_to_the_user']
            self.queue_management_system.enqueue(json_result['name'], json_result['urgency'])
            return f"{result} ({json_result['urgency']},{json_result['medical_specialty']})"
        else:
            return result

    def is_json_convertible(self, text: str) -> bool:
        """Check if a string is json convertible."""
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False
