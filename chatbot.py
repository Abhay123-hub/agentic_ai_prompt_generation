from typing import List
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel

from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AIMessage,HumanMessage,ToolMessage
from typing import Literal
from langgraph.graph import END

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph,START
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
import uuid
config = {"configurable": {"thread_id": str(uuid.uuid4())}}

class State(TypedDict):
    messages: Annotated[list,add_messages]

template = """  Your job is to get information from the user about what type of prompt template
they want to create .
You should get the following information from the user:
  - what objective of the prompt is
  - what variables will be passed into the prompt template
  - any constraints for what the output should not do
  - any requirements that the output must adhere to 
if you are not able to discern this info, ask the user to clarify! Do not attempt to wildly guess
after you are able to discern all the information ,call the relevant tool
  
  """

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo",api_key="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")


class PromptInstructions(BaseModel):
    """Instructions on how to prompt the LLM."""

    objective: str
    variables: List[str]
    constraints: List[str]
    requirements: List[str]

prompt = """ Based on the following requirements write a good prompt template
       {reqs} """


## defining my class

class chatbot:
    def __init__(self):
        self.llm = llm
        self.instructions = PromptInstructions
        self.template = template
        self.prompt = prompt
        self.State = State

    class State(TypedDict):
        messages: Annotated[list,add_messages]
        
    
    def info_chain(self,state:State):
        self.llm_bind_tools = llm.bind_tools([self.instructions])
        response = self.llm_bind_tools.invoke(state["messages"])
        return {"messages":[response]}
    def get_prompt_messages(self,messages:list):
        tool_call  = None
        other_msgs = []
        for m in messages:
            if isinstance(m,AIMessage) and m.tool_calls:
                tool_call = m.tool_calls[0]["args"]
            elif isinstance(m,ToolMessage):
                continue
            elif tool_call is not None:
                other_msgs.append(m)
        return [SystemMessage(content = prompt.format(reqs = tool_call))] + other_msgs
    
    def prompt_gen_chain(self,state:State):
        messages = self.get_prompt_messages(state["messages"])
        response = self.llm.invoke(messages)
        return {"messages":[response]}
    def get_state(self,state:State):
        messages = state["messages"]
        if isinstance(messages[-1],AIMessage) and messages[-1].tool_calls:
            return "add_tool_messages"
        elif not isinstance(messages[-1],HumanMessage):
            return END
        else:
            return "info"
    
    def __call__(self):
        """ set up the workflow for the chatbot"""
        memory = MemorySaver()
        workflow = StateGraph(State)

        workflow.add_node("info",self.info_chain)
        workflow.add_node("prompt",self.prompt_gen_chain)
        workflow.add_edge(START,"info")

        @workflow.add_node
        def add_tool_messages(state:State):
            return {
                "messages":[
                    ToolMessage(
                        content = "Prompt Generated!",
                        tool_call_id = state["messages"][-1].tool_calls[0]["id"],
                    )
                ]
            }
        
        ## adding condtional edges inside my graph
        workflow.add_conditional_edges("info",self.get_state,["add_tool_messages",END,"info"])
        workflow.add_edge("add_tool_messages","prompt")
        workflow.add_edge("prompt",END)

        graph = workflow.compile(checkpointer = memory)
        self.app = graph
        return self.app

if __name__ == "__main__":
    mybot = chatbot()
    workflow = mybot()
    inputs = {"messages":["give me the story of two friends working in coal mine get less pay but satisfied with family and happy"]}
    response = workflow.invoke(inputs,config = config)
    print(response["messages"][-1].content)
    

