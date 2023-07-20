from __future__ import annotations

from typing import Dict

from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.embeddings import GPT4AllEmbeddings
from genoss.model.base_genoss_llm import BaseGenossLLM
from genoss.chat.chat_completion import ChatCompletion


class Gpt4AllLLM(BaseGenossLLM):
    name: str = "gpt4all"
    description: str = "GPT-4"
    model_path: str = "./genoss/model/ggml-gpt4all-j-v1.3-groovy.bin"

    def generate_answer(self, messages: list) -> Dict:
        print("Generating Answer")
        print(messages)
        last_messages = messages

        llm = GPT4All(
            model=self.model_path,  # pyright: ignore reportPrivateUsage=none
        )
        prompt_template = "Question from user: {question}?, Answer from bot:"
        llm_chain = LLMChain(
            llm=llm, prompt=PromptTemplate.from_template(prompt_template)
        )
        response_text = llm_chain(last_messages)
        print("###################")
        print(response_text)
        answer = response_text["text"]
        chat_completion = ChatCompletion(
            model=self.name, answer=answer, last_messages=last_messages
        )

        return chat_completion.to_dict()

    def generate_embedding(self, embedding: str | list[str]):
        gpt4all_embd = GPT4AllEmbeddings()  # pyright: ignore reportPrivateUsage=none
        embedding_to_str = " ".join(embedding)
        return gpt4all_embd.embed_query(embedding_to_str)