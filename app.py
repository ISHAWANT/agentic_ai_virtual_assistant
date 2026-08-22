from langchain_openai import ChatOpenAI 
from langchain.tools import tool 
from langchain.agents import create_react_agent, AgentExecutor 

from langchain import hub 

from langchain_community.tools.tavily_search import TavilySearchResults 

from dotenv import load_dotenv 
import streamlit as st 
import requests 
import os 

load_dotenv() 

import os

WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# print(WEATHERSTACK_API_KEY)

if os.environ['TAVILY_API_KEY'] == os.getenv('TAVILY_API_KEY'): 
    print('Tavily API Key Loaded...')

if os.environ['WEATHERSTACK_API_KEY'] == os.getenv('WEATHERSTACK_API_KEY'):
    print('Weather API Key Loaded...')

if os.environ['OPENAI_API_KEY'] == os.getenv('OPENAI_API_KEY'):
    print('Open AI Loaded...')


if os.environ['OPENAI_BASE_URL'] == os.getenv('OPENAI_BASE_URL'):
    print('Open AI Base URL Loaded...')

# page config 

st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon='🤖',
    layout='centered'
) 

st.title('🤖 Agentic AI Virtual Assistant') 

st.markdown("🔎 **Search anything & get current weather updates**")

# search tool 

search_tool = TavilySearchResults(max_results=2) 

# weather tool 

@tool 
def get_weather(location: str) -> str:
    """Get the current weather for a given location.""" 

    url = (
        f"https://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query={location}"
    )

    res = requests.get(url) 

    data = res.json() 

    if "current" not in data:
        return f"Could not get weather for {location}. Please try again." 

    return f"The current weather in {location} is {data['current']['temperature']}°C with {data['current']['weather_descriptions'][0]}."

llm = ChatOpenAI(model='openai/gpt-3.5-turbo',
                 temperature=0.2,
                 ) 

prompt = hub.pull("hwchase17/react")

tools = [search_tool,get_weather] 

agent = create_react_agent(llm=llm, tools=tools,prompt=prompt) 

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

user_input = st.text_input(
    "Enter Your Query:",
    placeholder="Example: Find the current weather of Gaya, Bihar?"
)

if st.button('Get Answer'):
    if user_input:
        with st.spinner('Agent is working...'):
            try:
                res = agent_executor.invoke(
                    {'input':user_input}
                )

                st.success('Response Generated') 

                st.markdown("###Response: ") 

                st.write(res['output']) 

            except Exception as e:
                st.error(f"Error: {str(e)}")

    else:
        st.warning("Please Ask Your Question")