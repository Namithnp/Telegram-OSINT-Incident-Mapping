# Telegram-OSINT-Incident-Mapping

NOTE:
The project requires a pyrogram session login for Agent 1. 

### Problem Statement

Open-source intelligence (OSINT) from social platforms—especially Telegram—contains a massive volume of raw incident reports posted in real time. These messages are unstructured, duplicated across channels, geographically vague, and mixed with irrelevant chatter.
For an analyst or researcher, manually turning this firehose of unorganized text into meaningful, location-based insights is extremely slow and error-prone.

The core problem:
I wanted to create a system that can automatically convert chaotic Telegram messages into a clean, geospatially structured incident dataset, complete with categories, deduplicated events, and map-ready coordinates that can visually tell a story at a glance

Why this problem matters:

OSINT is increasingly important for understanding conflicts, disasters, security operations, and cross-border movements, all of which involve a geographic element.

Analysts often waste hours manually categorizing, geolocating, and filtering noise from useful intelligence.
A fully automated pipeline dramatically improves situational awareness, reduces analyst workload, and creates a replicable framework for future GEOINT/OSINT systems.

### Why agents? 

Automating the aggregation of information from different sources and routinely deriving an incident map can be simplified using agents that offer contextual help using natural language. Traditional solutions would involve the manual creation of a dataset required for mapping by curating text and classifying chunks of text to be used for map-based analysis. Using agents can minimize the time taken for the entire data preprocessing.
Thus, an “analyst voice” can lead the agentic pipeline — something purely deterministic code could never write convincingly.

### Architecture

**Agent 1 — Text Cleaner & Ingestor**

Telegram messages contain emojis, duplicates, forward markers, signatures, noise, etc.
A deterministic regex script fails here because cleaning depends on semantic understanding.
A dedicated LLM agent to fetch historic or current channel data makes accurate cleaning judgments and preserves meaning.

**Agent 2 — Geo-Significance Filter**

Not every post is a map-worthy incident.
This step requires reasoning, not rules.
For example:
“**Tension rising in the region**” → not an incident
“**IED blast in Pulwama town**” → mappable incident
An LLM agent is ideal for this kind of contextual classification.

**Agent 3 — Contextual Deduplicator**

Several channels often describe the same event with different words.
Rule-based similarity fails because:
- Locations are phrased differently
- Some posts are partial updates
- Some contain follow-ups

Only an LLM agent can assess whether two texts refer to the same real-world event on a given day.

**Agent 4 — Category & Location Extractor**

Extracting structured fields (category + geocodable location_text) from noisy messages requires:
- Semantic disambiguation
- Understanding the main subject
- Choosing the correct category from a closed label list
- Selecting a single, most precise location when only the approximate region is known
This is exactly the kind of task LLMs excel at.

**Agent 5 — LLM-Assisted Geocoder**
Instead of naive geocoding, this agent uses reasoning to:
- Refine vague region-level inputs into geocodable variants 
- Maintain specificity (avoid over-generalized coordinates)
- Prevent centroid drift by choosing logically consistent finer-grained locations
A hybrid of LLM reasoning + deterministic Google Maps API gives the best accuracy.

**Agent 6 — Reporter & Orchestrator**
Finally, one meta-agent:
- Uses a custom map generation tool
- Compiles the incident context
- Writes a polished, concise intelligence summary


### The Build

| Component               | Tool Used                               | Why                                                    |
| ----------------------- | --------------------------------------- | ------------------------------------------------------ |
| Fetching Telegram posts | **Pyrogram (async)**                    | Fast, reliable, handles user accounts                  |
| Data storage            | **SQLite**                              | Lightweight, stable, easy to inspect                   |
| Agents                  | **Google ADK (LlmAgent, FunctionTool)** | Modular agent design with tool integration             |
| LLMs                    | **Gemini 2.5 Flash / Flash-Lite**       | High-quality reasoning for classification & extraction |
| Maps                    | **Folium + GeoPandas**                  | Best interactive global mapping inside notebooks       |
| Geocoding               | **Google Maps API**                     | Accurate place lookup                                  |
| Notebook environment    | **Kaggle**                              | Clean, reproducible submission                         |

**Imports**
googlemaps
python-dotenv
pyrogram
tgcrypto
contextily
folium
geopandas
pandas
sqlite3
google-adk

### Further Enhancements
1. I would create a telegram bot that is interactive and can take date and channel input from the user to scrape public channels and produce output
2. Add memory service as a log to study how the LLM processes context from a large corpus of text, to write better system prompts for deduplication and category extraction
3. Use advanced spatial reasoning to geocode a particular location based on multiple location estimations of the same incident
