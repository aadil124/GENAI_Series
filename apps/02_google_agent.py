from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver    # save memory while chating

search = GoogleSerperAPIWrapper()

llm=ChatGroq(model="openai/gpt-oss-20b")

agent = create_agent(
    model=llm,
    tools=[search.run],
    system_prompt="your are a agent you can sreach any question on google",
    checkpointer=InMemorySaver()
)
# question = "What is the best Gen AI / Agentic AI series on Youtube"/
question = "Who won T20 World cup in 2024 and 2026"

while True:
    query=input("User: ")
    if query.lower() == "quit":
     print("Good Bye")
     break
    response=agent.invoke(
       {"messages":[{"role":"user","content":query}]},
       {"configurable": {"thread_id": "1"}},) 
    print(f"AI: ",response["messages"][-1].content)

