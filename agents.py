from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url 
from dotenv import load_dotenv

load_dotenv()

# Model setup 
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 1st Agent - Search Agent
def build_search_agent():
    tools = [web_search]
    
    # Tool-calling agents require an agent_scratchpad placeholder for history
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a research assistant tasked with searching for reliable information."),
        ("human", "{messages}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)

# 2nd Agent - Reader Agent
def build_reader_agent():
    tools = [scrape_url]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a web scraper assistant. You pick the best URL and scrape it for deep content."),
        ("human", "{messages}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)

# Writer Chain 
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

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain 
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

critic_chain = critic_prompt | llm | StrOutputParser()
