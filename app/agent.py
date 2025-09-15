# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIESs OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tool for finding nearby places using Google Maps API."""

import os
import googlemaps
from google.adk.tools import FunctionTool 

# --- CORRECTION 1: INITIALIZE THE CLIENT GLOBALLY ---
# Initialize the client one time when the module is loaded.
# This makes it efficient, as the function doesn't recreate it on every call.
# This assumes the GOOGLE_MAPS_API_KEY environment variable is set.
try:
    gmaps_client = googlemaps.Client(key=os.environ.get("GOOGLE_MAPS_API_KEY"))
except Exception as e:
    print(f"Error initializing Google Maps client: {e}")
    gmaps_client = None

# --- CORRECTION 2: CREATE A STANDALONE FUNCTION ---
# This function contains all the logic that was previously in the __call__ method.
# The docstring is critical: the agent reads it to understand what the tool
# does and what its arguments are.

def find_nearby_pharmacies(address: str) -> list[str]:
    """
    Finds nearby pharmacies for a given address.

    Args:
        address: The address to search around.

    Returns:
        A list of nearby pharmacies.
    """
    if not gmaps_client:
        return ["Google Maps client is not initialized. Check API key."]

    try:
        # Geocode the address using the global client
        geocode_result = gmaps_client.geocode(address)
        if not geocode_result:
            return ["Could not find the location for the given address."]

        location = geocode_result[0]["geometry"]["location"]
        lat = location["lat"]
        lng = location["lng"]

        # Find nearby pharmacies using the global client
        places_result = gmaps_client.places_nearby(
            location=(lat, lng),
            radius=5000,  # 5 kilometers
            type="pharmacy"
        )

        pharmacies = []
        for place in places_result.get("results", []):
            name = place.get("name")
            vicinity = place.get("vicinity")
            pharmacies.append(f"{name} at {vicinity}")

        return pharmacies if pharmacies else ["No pharmacies found nearby."]

    except Exception as e:
        return [f"An error occurred: {e}"]


# --- CORRECTION 3: WRAP THE FUNCTION ---
# You now create the tool object by passing your function to FunctionTool.
# This is the exact same pattern as your weather_agent script.
find_nearby_pharmacies_tool = FunctionTool(func=find_nearby_pharmacies)

# Now you can pass 'find_nearby_pharmacies_tool' (or even the raw
# function 'find_nearby_pharmacies' like your time_agent example)
# to your agent's tools list:
#
# my_agent = Agent(
#    ...
#    tools=[find_nearby_pharmacies_tool]
# )

"""Maps Agent: Finds nearby pharmacies."""

from google.adk.agents import LlmAgent

from . import maps_prompt


MODEL = "gemini-2.5-flash"


maps_agent = LlmAgent(
    name="maps_agent",
    model=MODEL,
    description="Finds nearby pharmacies for a given address.",
    instruction=maps_prompt.MAPS_AGENT_PROMPT,
    output_key="pharmacies",
    tools=[
        find_nearby_pharmacies_tool
    ],
)

root_agent = maps_agent
