import os
from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url

load_dotenv()


def get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is missing!")
    return ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)


def build_search_agent():
    tools = [web_search]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a research assistant tasked with searching for reliable information."),
        ("human", "{messages}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(get_llm(), tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)


def build_reader_agent():
    tools = [scrape_url]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a web scraper assistant. You pick the best URL and scrape it for deep content."),
        ("human", "{messages}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(get_llm(), tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)


def run_writer_chain(inputs: dict) -> str:
    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
        ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
    ])
    chain = writer_prompt | get_llm() | StrOutputParser()
    return chain.invoke(inputs)


def run_critic_chain(inputs: dict) -> str:
    critic_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a sharp and constructive research critic. Be honest and specific."),
        ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
    ])
    chain = critic_prompt | get_llm() | StrOutputParser()
    return chain.invoke(inputs)
