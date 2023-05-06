from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
import os
import re
import random
from langchain.memory import ConversationBufferWindowMemory

API_KEY = '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'
global tools
os.environ["GOOGLE_CSE_ID"] = "d52e4f02284464db8"
os.environ["GOOGLE_API_KEY"] = "AIzaSyAOAV_s4zOo9pjpXlFm28Ya-asMozeDMRU"
moods = [
    "happy",
    "sad",
    "angry",
    "excited",
    "bored",
    "tired",
]
search = GoogleSearchAPIWrapper()
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    global generated, past, entity_memory

    generated = []
    past = []
    entity_memory.entity_store = {}
    entity_memory.buffer.clear()

# Initialize session states
generated = []
past = []

# Create an OpenAI instance
llm = OpenAI(temperature=0,
            openai_api_key=API_KEY,
            model_name='gpt-3.5-turbo',
            verbose=False)
tool = Tool(
    name = "Google Search",
    description="Search Google for recent results.",
    func=search.run
)
entity_memory = ConversationEntityMemory(llm=llm, k=5)
memory = ConversationBufferWindowMemory( k=4)
# Create the ConversationChain object with the specified configuration
conversation = ConversationChain(
    llm=llm,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=entity_memory
)
prompt = """Answer the following questions as best you can. You have access to the following tools:

${tools}
Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [search, calculator]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: ${question}
Thought:"""
tools = {
    'gpt3' : {
        'description': "Useful for when you need to answer more general questions or emotional questions.",
        'execute': lambda user_input: conversation.run(input=user_input)
    },
    'search' :{
        'description': "Search Google for recent results.",
        'execute': lambda user_input: tool.run(tool_input=user_input)
    },
    'mood' : {
        'description': "Gets the users mood",
        'execute': lambda user_input: random_choice(moods, user_input)
    }
}
user_input = prompt.replace("${question}", "get the users mood")
user_input = user_input.replace("${tools}", "\n".join([f"{tool_name}: {tools[tool_name]['description']}" for tool_name in tools]))
output = conversation.run(input=user_input)

#         user_input = user_input.replace("${tools}", "\n".join([f"{tool_name}: {tools[tool_name]['description']}" for tool_name in tools]))
print(output)
# print("Welcome to the chat bot! Type 'history' to see past conversations, 'new' to start a new chat session, or 'exit' to quit.") 

def random_choice(list, user_input):
    return random.choice(list)


# while True:
#     user_input = input("You: ")

#     if user_input.lower() == 'new':
#         new_chat()
#     elif user_input.lower() == 'exit':
#         break
#     elif user_input.lower() == 'history':
#         print("Conversation History: ")
#         for i in range(0, len(past)):
#             print(past[i])
#             print(generated[i])
#     else:
#         user_input = prompt.replace("${question}", user_input)
#         user_input = user_input.replace("${tools}", "\n".join([f"{tool_name}: {tools[tool_name]['description']}" for tool_name in tools]))
#         output = conversation.run(input=user_input)
#         #output = tool.run(tool_input=user_input)
#         action_match = re.search(r"Action: (.*)", output)
#         action = action_match.group(1) if action_match else None

#         if action:
#             action_input_match = re.search(r"Action Input: (.*)", output)
#             action_input = action_input_match.group(1) if action_input_match else None

#             if action.strip() in tools:
#                 result = tools[action.strip()]['execute'](action_input)
#                 print(f"Result: {result}")
#                 prompt = prompt.replace("Observation", result)
#                 final_answer_match = re.search(r"Final Answer: (.*)", result)
#                 final_answer = final_answer_match.group(1) if final_answer_match else None
#             past.append(user_input)
#             generated.append(final_answer)
#         print("Bot: " + output)
        
# print("Goodbye!")