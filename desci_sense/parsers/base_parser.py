import os

from pathlib import Path
from typing import Optional, Dict
import desci_sense.configs as configs

from confection import Config

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from langchain.schema import (
    HumanMessage,
)


from ..twitter import scrape_tweet, extract_external_ref_urls
from ..utils import extract_and_expand_urls

from ..postprocessing.output_parsers import TagTypeParser




human_template = "{text}"


class BaseParser:
    def __init__(self, 
                 config: Config,
                 api_key: Optional[str]=None,
                 openapi_referer: Optional[str]=None
                 ) -> None:
        
        self.config = config
        
        # if no api key passed as arg, default to environment config
        openai_api_key = api_key if api_key else os.environ["OPENROUTER_API_KEY"]
        
        openapi_referer = openapi_referer if openapi_referer else os.environ["OPENROUTER_REFERRER"]


        # init model
        model_name = "mistralai/mistral-7b-instruct" if not "name" in config["model"] else config["model"]["name"]
        
        self.model = ChatOpenAI(
            model=model_name, 
            temperature=self.config["model"]["temperature"],
            openai_api_key=openai_api_key,
            openai_api_base=configs.OPENROUTER_API_BASE,
            headers={"HTTP-Referer": openapi_referer}, 
        )

        # load prompt
        template_path = Path(__file__).parents[2] / self.config["prompt"]["template_path"]
        template = template_path.read_text()

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", human_template),
        ])

        self.output_parser = TagTypeParser()

        self.chain = self.prompt_template | self.model | self.output_parser
        
    def process_text(self, text: str):
        # print("Text received: ", text)
        # process tweet in the format of the output of scrape_tweet

        answer = self.chain.invoke({"text": text})

        # check if there is an external link in this post - if not, tag as <no-ref>
        # expanded_urls = extract_and_expand_urls(text)

        # if not expanded_urls:
        #     answer = {"reasoning": "[System msg: no urls detected - categorizing as <no-ref>]", 
        #                      "final_answer": "<no-ref>"}
        # else:
        #     # url detected, process to find relation of text to referenced url
        #     answer = self.chain.invoke({"text": text})

        # TODO fix results
        result = {"text": text,
                  "answer": answer
                  }

        return result
    
    def process_tweet(self, tweet: Dict):
        # process tweet in the format of the output of scrape_tweet

        # answer = self.chain.invoke({"text": tweet["text"]})

        # check if there is an external link in this post - if not, tag as <no-ref>
        expanded_urls = extract_external_ref_urls(tweet)

        if not expanded_urls:
            answer = {"reasoning": "[System msg: no urls detected - categorizing as <no-ref>]", 
                             "final_answer": "<no-ref>"}
        else:
            # url detected, process to find relation of text to referenced url
            answer = self.chain.invoke({"text": tweet["text"]})

        result = {"tweet": tweet,
                  "answer": answer
                  }

        return result



    def process_tweet_url(self, tweet_url: str):

        # get tweet in json format
        tweet = scrape_tweet(tweet_url)

        # check if there is an external link in this post - if not, tag as <no-ref>
        expanded_urls = extract_external_ref_urls(tweet)

        

        if not expanded_urls:
            answer = {"reasoning": "[System msg: no urls detected - categorizing as <no-ref>]", 
                             "final_answer": "<no-ref>"}
        else:
            # url detected, process to find relation of text to referenced url
            answer = self.chain.invoke({"text": tweet["text"]})

        
        result = {"tweet": tweet,
                  "answer": answer
                  }

        return result








