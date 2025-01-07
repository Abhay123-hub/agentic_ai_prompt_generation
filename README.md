# Chatbot Prompt Generator using LangChain and LangGraph

This project implements a chatbot system that helps users create a custom prompt template for a specific objective. The system uses LangChain for model invocation and LangGraph for managing workflows.

## Features

- **Chatbot Workflow**: The chatbot guides users through specifying the objective of a prompt template, the variables that will be used, constraints, and requirements.
- **Prompt Generation**: Based on the user input, the chatbot generates a custom prompt template by utilizing LangChain's language models (such as GPT-3.5-turbo).
- **State Management**: The chatbot uses a state graph to handle the flow of messages, processing different types of inputs such as user queries and AI responses.

## Requirements

- Python 3.7 or higher
- `langchain`, `langgraph`, `pydantic`, `uuid`, `typing`, `typing_extensions`, `langchain_openai`, `langchain_groq`, `langgraph_core`

You can install the required dependencies using:

```bash
pip install -r requirements.txt


Setup
Configure OpenAI API Key: In the code, ensure that you replace the api_key in the ChatOpenAI initialization with your actual OpenAI API key.

Run the chatbot: To start the chatbot, run the script:

python chatbot_prompt_generator.py

python chatbot_prompt_generator.py

Test the chatbot: You can interact with the chatbot by providing a list of messages in the format

inputs = {"messages": ["Give me the story of two friends working in a coal mine, getting less pay but satisfied with family and happy."]}
response = workflow.invoke(inputs, config=config)
print(response["messages"][-1].content)

Code Explanation
State: A TypedDict that holds the state of the chatbot, including the messages exchanged.
PromptInstructions: A Pydantic model that defines the required instructions for generating a prompt, including the objective, variables, constraints, and requirements.
chatbot class:
Initializes the necessary components, including the language model (llm), instructions, and prompt templates.
Defines the workflow using StateGraph and adds nodes for processing user input, generating prompts, and invoking tools.
The workflow also includes conditional edges that determine the next steps based on the state of the chatbot.
info_chain: Retrieves instructions from the user about the prompt template and feeds it into the language model.
prompt_gen_chain: Generates the prompt template based on the collected instructions.
get_state: Determines the next action based on the last message in the conversation.
Example Flow
The user provides a message that describes their prompt requirements.
The system collects information about the prompt's objective, variables, constraints, and requirements.
The chatbot generates the appropriate prompt based on the information.
The workflow completes the process, returning a response to the user.
Contributing
Feel free to fork the repository and make your contributions! Ensure you follow best practices for code quality and testing.