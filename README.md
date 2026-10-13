# TravelWithMe ✈️

A conversational AI travel concierge agent that helps travelers discover destinations, plan trips, and explore activities tailored to their preferences and budget.

Built with Google ADK (Agent Development Kit), Gemini 3.8 Flash, and Cloud Firestore.

## Features

- 🧭 **Curated Destination Catalog**: Powered by a Google Cloud Firestore backend (`destinations` collection).
- 🔍 **Smart Destination Filtering**: `list_destinations` allows searching by travel style (cultural, adventure, nature, culinary, urban) and maximum daily budget.
- 📋 **Detailed Travel Insights**: `get_destination_details` fetches activities, seasonal recommendations, average costs, and ratings.
- ✍️ **Catalog Updates**: `add_destination` enables saving new destinations to the database.
- 🌦️ **Trip Logistics**: Built-in tools for weather checks and local time zones.

## Project Structure

```
travel-with-me/
├── app/
│   ├── agent.py               # Root agent definition & instruction
│   ├── tools.py               # Firestore integration & function tools
│   ├── fast_api_app.py        # FastAPI A2A backend server
│   └── app_utils/             # App utilities and helpers
├── scripts/
│   └── seed_firestore.py      # Firestore seeding script with sample destinations
├── project_brief.md           # Agent design brief and tool coverage
├── tests/                     # Unit and integration tests
├── GEMINI.md                  # Development guide & operational guidelines
└── pyproject.toml             # Dependencies (ADK, Firestore, FastAPI)
```

## Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Seed Firestore Catalog

```bash
uv run python scripts/seed_firestore.py
```

### 3. Run the Agent Locally

Run the interactive local development playground:

```bash
agents-cli playground
```
