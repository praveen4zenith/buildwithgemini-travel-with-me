# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

try:
    from .tools import add_destination, get_destination_details, list_destinations
except ImportError:
    from tools import add_destination, get_destination_details, list_destinations



MODEL = "gemini-3.8-flash"


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        query: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    q = query.lower()
    if "sf" in q or "san francisco" in q:
        tz_identifier = "America/Los_Angeles"
    elif "hyderabad" in q or "india" in q or "kolkata" in q or "delhi" in q or "mumbai" in q or "bangalore" in q or "bengaluru" in q:
        tz_identifier = "Asia/Kolkata"
    elif "new york" in q or "nyc" in q:
        tz_identifier = "America/New_York"
    elif "london" in q:
        tz_identifier = "Europe/London"
    elif "tokyo" in q:
        tz_identifier = "Asia/Tokyo"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are TravelWithMe, an expert AI travel concierge. You help travelers discover destinations, "
        "plan trips, and explore activities tailored to their preferences and budget.\n\n"
        "Use your Firestore travel catalog tools:\n"
        "- `list_destinations`: Search and filter destinations by travel style or maximum budget.\n"
        "- `get_destination_details`: Retrieve full details, activities, and seasonal recommendations for a destination.\n"
        "- `add_destination`: Add new travel destinations or update existing ones in the catalog.\n\n"
        "You also have `get_weather` and `get_current_time` to assist with trip logistics."
    ),
    tools=[get_weather, get_current_time, list_destinations, get_destination_details, add_destination],
)

app = App(
    root_agent=root_agent,
    name="app",
)
