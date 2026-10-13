#!/usr/bin/env python3
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

"""Seeds sample travel destinations into Cloud Firestore for TravelWithMe."""

from google.cloud import firestore

# Explicitly hardcoded GCP project ID
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-03-fd1a6864763d"
COLLECTION_NAME = "destinations"

SAMPLE_DESTINATIONS = [
    {
        "id": "tokyo-japan",
        "name": "Tokyo",
        "country": "Japan",
        "description": "A vibrant metropolis blending futuristic skyscrapers, historic temples, neon-lit nightlife, and world-renowned gastronomy.",
        "travel_style": ["urban", "cultural", "culinary", "shopping"],
        "budget_tier": "moderate",
        "best_seasons": ["spring", "autumn"],
        "top_activities": [
            "Explore Tsukiji Outer Market street food",
            "Visit Senso-ji Temple in Asakusa",
            "Take in panoramic city views at Shibuya Sky",
            "Stroll the serene grounds of Meiji Shrine",
        ],
        "average_daily_cost_usd": 180.0,
        "rating": 4.9,
    },
    {
        "id": "kyoto-japan",
        "name": "Kyoto",
        "country": "Japan",
        "description": "The cultural heart of Japan, famous for thousand-year-old wooden temples, peaceful Zen rock gardens, traditional tea houses, and geisha districts.",
        "travel_style": ["cultural", "relaxation", "historical"],
        "budget_tier": "moderate",
        "best_seasons": ["spring", "autumn"],
        "top_activities": [
            "Walk through thousands of torii gates at Fushimi Inari-taisha",
            "Stroll the soaring bamboo grove in Arashiyama",
            "Attend an authentic matcha tea ceremony in Gion",
            "Marvel at Kinkaku-ji (The Golden Pavilion)",
        ],
        "average_daily_cost_usd": 160.0,
        "rating": 4.8,
    },
    {
        "id": "banff-canada",
        "name": "Banff",
        "country": "Canada",
        "description": "A picturesque resort town inside Banff National Park in the Canadian Rockies, famous for turquoise glacial lakes, rugged peaks, and wildlife.",
        "travel_style": ["adventure", "nature", "outdoor"],
        "budget_tier": "moderate",
        "best_seasons": ["summer", "winter"],
        "top_activities": [
            "Canoe across the glacial waters of Lake Louise and Moraine Lake",
            "Hike the Plain of Six Glaciers trail",
            "Soak in Banff Upper Hot Springs with mountain views",
            "Drive the scenic Icefields Parkway",
        ],
        "average_daily_cost_usd": 210.0,
        "rating": 4.9,
    },
    {
        "id": "florence-italy",
        "name": "Florence",
        "country": "Italy",
        "description": "The cradle of the Renaissance, renowned for masterpieces of art, the iconic terracotta-tiled Duomo, Tuscan culinary wonders, and cobblestone charm.",
        "travel_style": ["cultural", "culinary", "historical", "romantic"],
        "budget_tier": "moderate",
        "best_seasons": ["spring", "autumn"],
        "top_activities": [
            "Climb Brunelleschi's Dome at Florence Cathedral",
            "Admire Michelangelo's David at Galleria dell'Accademia",
            "Catch the sunset over Ponte Vecchio from Piazzale Michelangelo",
            "Savor authentic pasta and Chianti wine tasting in San Frediano",
        ],
        "average_daily_cost_usd": 195.0,
        "rating": 4.8,
    },
    {
        "id": "costa-rica-arenal",
        "name": "Arenal & La Fortuna",
        "country": "Costa Rica",
        "description": "An eco-adventure paradise set around the dramatic Arenal Volcano, surrounded by lush rainforests, natural thermal hot springs, and rich wildlife.",
        "travel_style": ["adventure", "nature", "relaxation", "wildlife"],
        "budget_tier": "budget",
        "best_seasons": ["winter", "spring"],
        "top_activities": [
            "Hike the 1968 lava flow trails around Arenal Volcano",
            "Zipline high above the tropical rainforest canopy",
            "Soak in natural thermal hot springs along the Tabacon river",
            "Swim under the 70-meter cascade at La Fortuna Waterfall",
        ],
        "average_daily_cost_usd": 120.0,
        "rating": 4.7,
    },
]


def seed_database() -> None:
    print(f"Connecting to Firestore for project: '{FIRESTORE_PROJECT_ID}'...")
    db = firestore.Client(project=FIRESTORE_PROJECT_ID)
    collection_ref = db.collection(COLLECTION_NAME)

    print(f"Seeding {len(SAMPLE_DESTINATIONS)} destinations into '{COLLECTION_NAME}'...")
    for item in SAMPLE_DESTINATIONS:
        doc_id = item["id"]
        data = {k: v for k, v in item.items() if k != "id"}
        collection_ref.document(doc_id).set(data, merge=True)
        print(f"  ✓ Seeded: {item['name']} ({doc_id})")

    print("\nDatabase seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
