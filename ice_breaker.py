# from dotenv import load_dotenv;
# import os;
#
# if __name__ == '__main__':
#     load_dotenv();
#     print("Hello LangChain! Rushik Soni")
#     print(os.environ['COOL_API_KEY'])

##### S2-L11:- Prompt Template LLM
from langchain_core.output_parsers import StrOutputParser

# Main Code ---------
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama
#
# from third_parties.linkedin import scrape_linkedin_profile
# from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
# from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
# from third_parties.twitter import scrape_user_tweets
# from output_parsers import summary_parser
#
# def ice_break_with(name: str) -> str:
#     linkedin_username = linkedin_lookup_agent(name=name)
#     linkedin_data=scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)
#
#     twitter_username = twitter_lookup_agent(name=name)
#     tweets = scrape_user_tweets(username=twitter_username, mock=True)
#
#     summary_template = """
#         given the information about a person from linkedin {information},
#         and their latest twitter posts {twitter_posts} I want you to create:
#         1. A short summary
#         2. two interesting facts about them
#
#         Use both information from twitter and Linkedin
#         \n{format_instructions}
#         """
#     summary_prompt_template = PromptTemplate(
#         # input_variables=["information", "twitter_posts"], template=summary_template
#
#         input_variables=["information", "twitter_posts"],
#         template=summary_template,
#         partial_variables = {
#             "format_instructions": summary_parser.get_format_instructions()
#         }
#     )
#     llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
#     # llm = ChatOllama(model="llama3")
#
#     # chain = summary_prompt_template | llm | StrOutputParser()
#     chain = summary_prompt_template | llm | summary_parser
#
#     # res = chain.invoke(input={"information": linkedin_data})
#     res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})
#
#     print(res)
#
#
# information = '''
#     Pichai Sundararajan (born June 10, 1972), better known as Sundar Pichai,[a] is an Indian-born American business executive.[3][4] He is the chief executive officer of Alphabet Inc. and its subsidiary Google.[5]
#
# Pichai began his career as a materials engineer. Following a short stint at the management consulting firm McKinsey & Co., Pichai joined Google in 2004,[6] where he led the product management and innovation efforts for a suite of Google's client software products, including Google Chrome and ChromeOS, as well as being largely responsible for Google Drive. In addition, he went on to oversee the development of other applications such as Gmail and Google Maps. In 2010, Pichai also announced the open-sourcing of the new video codec VP8 by Google and introduced the new video format, WebM. The Chromebook was released in 2012. In 2013, Pichai added Android to the list of Google products that he oversaw.
#
# Pichai was selected to become the next CEO of Google on August 10, 2015, after previously being appointed chief product officer by then CEO Larry Page. On October 24, 2015, he stepped into the new position at the completion of the formation of Alphabet Inc., the new holding company for the Google company family. He was appointed to the Alphabet Board of Directors in 2017.[7]
# '''
#
# if __name__ == '__main__':
#     print("Hello Rushik !!!")
#
#     print("ice break called!")
#
#     ice_break_with(name="Rushik Ghuntala")
#
#     # summary_template= '''
#     #     given LinkedIn information {information} about person from i want to create with list and title:
#     #     1. Short Summary
#     #     2. One interesting facts about them
#     # '''
#     #
#     # summary_prompt_template = PromptTemplate(
#     #     input_variables=["information"], template=summary_template
#     # )
#     #
#     # # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
#     # llm = ChatOllama(model="llama3")
#     # llm = ChatOllama(model="mistral")
#
#     # chain = summary_prompt_template | llm | StrOutputParser()
#
#     # linkedin_data = scrape_linkedin_profile(
#     #     linkedin_profile_url='https://www.linkedin.com/in/rushik-ghuntala-4a165222a/'
#     # )
#
#     # res = chain.invoke(input={"information": information})
#     # res = chain.invoke(input={"information": linkedin_data})
#
#     # print("Res: ", res)
#


from typing import Tuple

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.twitter import scrape_user_tweets
from output_parsers import summary_parser, Summary


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=False
    )

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)

    summary_template = """
    given the information about a person from linkedin {information},
    and their latest twitter posts {twitter_posts} I want you to create:
    1. A short summary
    2. two interesting facts about them 

    Use both information from twitter and Linkedin
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    ice_break_with(name="Harrison Chase")
