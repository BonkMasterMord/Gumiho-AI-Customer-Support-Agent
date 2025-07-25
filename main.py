from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool, company_info_tool
load_dotenv()

#llm = ChatOpenAI(model="gpt-4o-mini")  <-- for OpenAI API

# Pydantic model
class ResearchResponse(BaseModel):
# specify fields of what you want as output from your LLM call
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    
# Specify the model you want to use
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# The "Wrap the output in this format" is the format that the LLM will return the response in
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a customer service provider that will help answer questions that clients or customers may have from Gumiho LLC.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"), # necessary for the agent to understand the query
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Define the tools to be used by the agent (i.e. wiki_tool, save_tool)
tools = [search_tool, wiki_tool, save_tool, company_info_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)
# passing the tools to the agent executor
# verbose=True will print the agent's thought process setting it to Fakse will prevent it from printing
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can I help you with? ")
raw_response = agent_executor.invoke({"query": query})

try:
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)