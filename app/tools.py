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

"""Firestore backend tools for the TravelWithMe travel concierge agent."""

from typing import Any
from google.cloud import firestore

# Explicitly hardcoded GCP project ID (avoid google.auth.default() / GOOGLE_CLOUD_PROJECT
# which can return the project number on Agent Platform).
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-03-fd1a6864763d"
COLLECTION_NAME = "destinations"

_client: firestore.Client | None = None


def get_firestore_client() -> firestore.Client:
    """Returns a singleton Firestore client instance."""
    global _client
    if _client is None:
        _client = firestore.Client(project=FIRESTORE_PROJECT_ID)
    return _client


def list_destinations(travel_style: str = "", max_budget_usd: float = 0.0) -> list[dict[str, Any]]:
    """Fetches and searches destinations from the catalog in Firestore.

    Args:
        travel_style: Optional travel style keyword to filter by (e.g. 'adventure', 'cultural', 'nature', 'culinary', 'urban').
        max_budget_usd: Optional maximum average daily cost filter in USD.

    Returns:
        A list of destination dictionaries matching the query criteria.
    """
    db = get_firestore_client()
    docs = db.collection(COLLECTION_NAME).stream()

    results: list[dict[str, Any]] = []
    style_filter = travel_style.strip().lower()

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id

        # Filter by style if provided
        if style_filter:
            styles = [s.lower() for s in data.get("travel_style", [])]
            if not any(style_filter in s for s in styles):
                continue

        # Filter by max budget if provided
        if max_budget_usd > 0.0:
            daily_cost = data.get("average_daily_cost_usd", 0.0)
            if daily_cost > max_budget_usd:
                continue

        results.append(data)

    return results


def get_destination_details(destination_id: str) -> dict[str, Any]:
    """Fetches detailed information for a specific destination by its ID.

    Args:
        destination_id: The unique identifier of the destination (e.g., 'tokyo-japan', 'kyoto-japan', 'banff-canada').

    Returns:
        A dictionary containing the full destination details, or an error message if not found.
    """
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(destination_id)
    doc = doc_ref.get()

    if not doc.exists:
        return {"error": f"Destination with ID '{destination_id}' not found."}

    data = doc.to_dict() or {}
    data["id"] = doc.id
    return data


def add_destination(
    destination_id: str,
    name: str,
    country: str,
    description: str,
    travel_style: list[str],
    budget_tier: str,
    best_seasons: list[str],
    top_activities: list[str],
    average_daily_cost_usd: float,
    rating: float = 4.5,
) -> str:
    """Adds or updates a destination in the Firestore travel catalog.

    Args:
        destination_id: Unique slug/id for the destination (e.g., 'florence-italy').
        name: City or destination name (e.g., 'Florence').
        country: Country name (e.g., 'Italy').
        description: Overview description of what makes this destination special.
        travel_style: List of travel style tags (e.g., ['cultural', 'culinary', 'historical']).
        budget_tier: Budget tier ('budget', 'moderate', 'luxury').
        best_seasons: Recommended seasons to visit (e.g., ['spring', 'autumn']).
        top_activities: Highlights and key activities.
        average_daily_cost_usd: Estimated average daily expenses in USD.
        rating: Overall traveler rating (1.0 to 5.0).

    Returns:
        A status message confirming the destination was saved.
    """
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(destination_id)

    data = {
        "name": name,
        "country": country,
        "description": description,
        "travel_style": travel_style,
        "budget_tier": budget_tier,
        "best_seasons": best_seasons,
        "top_activities": top_activities,
        "average_daily_cost_usd": average_daily_cost_usd,
        "rating": rating,
    }

    doc_ref.set(data, merge=True)
    return f"Successfully saved destination '{name}' ({destination_id}) to Firestore."
