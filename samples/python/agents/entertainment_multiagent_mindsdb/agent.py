import os

from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools import google_search


movies_agent = RemoteA2aAgent(
    name='movies_agent',
    url=f'https://7625f341f0ff.ngrok-free.app/a2a{AGENT_CARD_WELL_KNOWN_PATH}',
)

tv_agent = Agent(
    name='tv_agent',
    model='gemini-2.5-flash-lite',
    description=('Agent to give TV show recommendations.'),
    instruction=(
        'You are a helpful agent who can provide engaging TV show recommendations.'
    ),
    tools=[google_search],
)

music_agent = Agent(
    name='music_agent',
    model='gemini-2.5-flash-lite',
    description=('Agent to give music recommendations.'),
    instruction=(
        'You are a helpful agent who can provide engaging music recommendations.'
    ),
    tools=[google_search],
)

video_games_agent = Agent(
    name='video_games_agent',
    model='gemini-2.5-flash-lite',
    description=('Agent to give video game recommendations.'),
    instruction=(
        'You are a helpful agent who can provide engaging video game recommendations.'
    ),
    tools=[google_search],
)

root_agent = Agent(
    name='entertainment_agent',
    model='gemini-2.5-flash-lite',
    description=(
        'Agent to give entertainment recommendations across movies, music, TV, video games, etc.'
    ),
    instruction=(
        'You are a helpful agent who can provide engaging entertainment recommendations. You can suggest movies, music, TV shows, video games, and more based on user preferences.'
    ),
    sub_agents=[movies_agent, tv_agent, music_agent, video_games_agent],
)

a2a_app = to_a2a(root_agent, port=int(os.getenv('PORT', '8001')))
