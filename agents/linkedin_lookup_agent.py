import os
from dotenv import load_dotenv
from langchain.chains.summarize.map_reduce_prompt import prompt_template
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import(
    create_react_agent,
    AgentExecutor
)
from langchain import hub

from tools.tool import get_profile_url_tavily

load_dotenv()

def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
    )
    # llm = ChatOllama(model="llama3")
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                                  Your answer should contain only a URL"""
    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name_of_person"]
    )
    # implement tool for agent
    tools_for_agents=[
        Tool(
            name="Crawl Google 4 LinkedIn Profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the LinkedIn Page URL",
        )
    ]

    # we are using prompt which is made by hw (Harrison)
    react_prompt = hub.pull("hwchase17/react")

    # implement agent
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agents,
        prompt=react_prompt
    )

    # run time executor of agent
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agents,
        verbose=True
    )

    # acquire result
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    # parse out the result
    linkedin_profile_url = result["output"]
    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url = lookup(name="Rushik Ghuntala")
    print(linkedin_url)