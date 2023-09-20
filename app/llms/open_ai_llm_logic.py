from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import (
    SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
)
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import Any
from app.llms import llm_logic
from app.llms.token_cost_process import CostCalcAsyncHandler, TokenCostProcess


# Desired output format.
class MedicalSpecialty(BaseModel):
    medical_specialty: str = Field(description="medical specialty the patient should go to")
    urgent: bool = Field(description="the patient should go to the hospital immediately")


parser = PydanticOutputParser(pydantic_object=MedicalSpecialty)  # type: ignore

# system message prompt. It defines the instructions for the system.
template: str = """You are a medical expert.
            You will receive the symptoms and will tell the medical specialty the patient should go to.
            {format_instructions}"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)


class OpenAILLMLogic(llm_logic.LLMLogic):
    """
    Implementation of the client that is responsible for the logic of the LLM.
    """

    def __enter__(self) -> "OpenAILLMLogic":
        self.token_cost_process = TokenCostProcess()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        print(self.token_cost_process.get_cost_summary("gpt-3.5-turbo"))

    async def chat(self, prompt: str) -> str:
    
        llm = ChatOpenAI(temperature=0, callbacks=[CostCalcAsyncHandler("gpt-3.5-turbo", self.token_cost_process)])

        chain = LLMChain(llm=llm, prompt=chat_prompt)

        result: str = await chain.arun({'text': prompt, 'format_instructions': parser.get_format_instructions()})

        return result
