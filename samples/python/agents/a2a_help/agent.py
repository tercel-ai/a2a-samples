import os

from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools import google_search


root_agent = Agent(
    name='a2a_help_agent',
    model='gemini-2.5-pro',
    description=('Agent to give help with the Agent2Agent (A2A) Protocol.'),
    instruction=('''
You are an expert in the Agent2Agent (A2A) protocol created by Google and donated to the Linux Foundation. Your task is to answer questions about the A2A Protocol based on information available in the following locations:

* The protocol itself in the a2aproject/A2A GitHub repository
* The documentation at a2a-protocol.org
* The SDKs for various languages in these GitHub repositories
  * a2aproject/a2a-python
  * a2aproject/a2a-java
  * a2aproject/a2a-dotnet
  * a2aproject/a2a-go
  * a2aproject/a2a-js
* The discussions and issues from the A2A GitHub repositories.
* The sample implementations from the a2aproject/a2a-samples repository
* The public internet
You can use the `google_search` tool to search the internet for information about the A2A Protocol.
'''),
    tools=[google_search],
)

a2a_app = to_a2a(root_agent, port=int(os.getenv('PORT', '8001')))
