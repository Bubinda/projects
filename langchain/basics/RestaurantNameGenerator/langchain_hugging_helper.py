from secret_key import hugging_token
import os
from langchain.chains import SequentialChain
from langchain import HuggingFaceHub, LLMChain
from langchain.prompts import PromptTemplate


os.environ['HUGGINGFACEHUB_API_TOKEN'] = hugging_token



# for the Hugginface Hub API -> no local model
# for the localmodel the HuggingFacePipeline should be used:
# reffer to https://python.langchain.com/docs/integrations/providers/huggingface
# another good block: https://blog.futuresmart.ai/integrating-llama-2-with-hugging-face-and-langchain

hub_llm_zephyr = HuggingFaceHub(repo_id="HuggingFaceH4/zephyr-7b-alpha")
hub_llm_mistral = HuggingFaceHub(repo_id="mistralai/Mistral-7B-v0.1")

def generate_chains_and_run(cuisine: str):

    prompt_template_name = PromptTemplate(
        input_variables =['cuisine'],
        template = "I want to open a restaurant for {cuisine} food. Suggest a fency name for this."
    )

    name_chain_zephyr =LLMChain(llm=hub_llm_zephyr, prompt=prompt_template_name, output_key="restaurant_name")
    name_chain_mistral =LLMChain(llm=hub_llm_mistral, prompt=prompt_template_name, output_key="restaurant_name")


    prompt_template_items = PromptTemplate(
        input_variables = ['restaurant_name'],
        template="Suggest some menu items for {restaurant_name}."
    )

    food_items_chain_zephyr =LLMChain(llm=hub_llm_zephyr, prompt=prompt_template_items, output_key="menu_items")
    food_items_chain_mistral =LLMChain(llm=hub_llm_mistral, prompt=prompt_template_items, output_key="menu_items")



    chain_1 = SequentialChain(
        chains = [name_chain_zephyr, food_items_chain_zephyr],
        input_variables = ['cuisine'],
        output_variables = ['restaurant_name', "menu_items"]
    )

    chain_2 = SequentialChain(
        chains = [name_chain_mistral, food_items_chain_mistral],
        input_variables = ['cuisine'],
        output_variables = ['restaurant_name', "menu_items"]
    )


    zephyr_out = chain_1({"cuisine": cuisine})
    mistral_out = chain_2({"cuisine": cuisine})

    return zephyr_out