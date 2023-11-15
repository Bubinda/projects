from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
import os

from dotenv import load_dotenv
import chainlit as cl

# Load environment variables from .env file
load_dotenv()


HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

#repo_id = "tiiuae/falcon-7b-instruct"
# repo_id = "HuggingFaceH4/zephyr-7b-beta"
# llm = HuggingFaceHub(huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN, 
#                      repo_id=repo_id, 
#                      model_kwargs={"temperature":0.7, "max_new_tokens":500})


# template = """
# You are a helpful AI assistant and provide the answer for the question asked politely.

# {question}
# Answer: Let's think step by step.
# """

# @cl.on_chat_start
# def main():
#     # Instantiate the chain for that user session
#     prompt = PromptTemplate(template=template, input_variables=["question"])
#     llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

#     # Store the chain in the user session
#     print(llm_chain.run(prompt))
#     cl.user_session.set("llm_chain", llm_chain)

# @cl.on_message
# async def main(message: str):
#     # Retrieve the chain from the user session
#     llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

#     # Call the chain asynchronously
#     res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

#     # Do any post processing here

#     # Send the response
#     await cl.Message(content=res["text"]).send()

@cl.on_chat_start
async def on_chat_start():
    repo_id = "HuggingFaceH4/zephyr-7b-beta"
    model = HuggingFaceHub(huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN, 
                         repo_id=repo_id, 
                         model_kwargs={"temperature":0.7, "max_new_tokens":500})
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very knowledgeable and helpfull assistant that loves to answer all the qeustions from the user and gives kind answers.",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()