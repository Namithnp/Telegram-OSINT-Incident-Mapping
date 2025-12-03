# Telegram-OSINT-Incident-Mapping

### IMPORTANT NOTE:

This project fetches messages using **Pyrogram (MTProto)**. To run the live pipeline you **must** provide your own Telegram API credentials and log in with *your* Telegram account.

1. Create Telegram API credentials at https://my.telegram.org → API development tools  
   - You will get **API_ID** and **API_HASH** used in the project
     
2. When you run the Pyrogram client for the first time it will prompt you for your phone number and a login code sent by Telegram. This authenticates *your* account locally and creates a session file on your computer.

3. This project reads messages from specific OSINT Telegram channels. To reproduce the live fetch you must **join the same channels** in your Telegram account (Or change the channels list in the code and add your preferred OSINT channels):

Channels used:
- @OsintTV (chat id: -1001554189930)
- @WarAndGore (chat id: -1001964457167)
- @ElitePredators (chat id: -1001150168882)
- @ResonantNews (chat id: -1001407087072)

API Requirements:
1. Telegram API ID
2. Telegram API Hash
3. Gemini API Key
4. Google Maps API Key  

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

**Multi-Agent System**

This project implements a complete, end-to-end OSINT analysis pipeline where each stage is handled by a dedicated autonomous agent. Instead of using a single LLM prompt, I decomposed the workflow into six agents that collaborate implicitly through a shared database: a cleaning agent, an incident-classification agent, a contextual deduplication agent, a category/location extractor, an LLM-assisted geocoder, and a reporter-map-orchestrator. Each agent has a narrowly defined role, its own system instructions, and transforms the dataset in a structured, sequential manner. This mirrors real-world intelligence pipelines where different analyst teams focus on specific layers of abstraction (noise removal, event validation, clustering, structuring, geolocation, reporting). Because each agent only sees the context relevant to its task, the system stays modular, interpretable, and easy to debug or extend—a hallmark of a genuine multi-agent architecture rather than a single LLM operating in disguise. The notebook demonstrates these agents executing asynchronously, updating the database, and handing off work to the next stage, fulfilling the core requirement of multi-stage agent collaboration.

**Custom Tools**

The project also demonstrates the use of custom tools—another explicit requirement of the competition. Several functions are exposed as tools that agents can call, most importantly the LLM-assisted geocoder and the interactive map generator. The geocoder combines reasoning-based location disambiguation with deterministic Google Maps lookup, wrapped as a callable tool that Agents can trigger when needed. Agent 6 uses a FunctionTool interface to generate interactive global maps directly inside the notebook, allowing the LLM to orchestrate data visualization without embedding code in its outputs. Beyond these, utilities for database operations, record fetching, and data segmentation act as additional custom tools that modularize the workflow. By integrating LLM reasoning with these purpose-built tools, the project moves beyond simple text generation and demonstrates how agents can perform real operations inside a controlled execution environment. This blend of cognitive agents and functional tools is exactly what the competition aims to showcase.

**Context Engineering**

Elaborate and articulate system prompts are set for each agent that creates a rigid schema of expected model response. The pipeline is heavily driven by deliberate context engineering, which ensures that each agent receives only the information required for its stage. Instead of giving raw Telegram messages to every agent, the system gradually refines and structures the context as it flows downstream: Agent 1 supplies cleaned text; Agent 2 consumes only those fields to determine geo-significance; Agent 3 receives date-segmented messages to make deduplication tractable; Agent 4 receives canonical messages along with minimal metadata; Agent 5 receives only a location text to interpret; and Agent 6 receives a distilled, global view summarizing in-region and out-of-region incidents. This progressive refinement prevents hallucination, keeps agents aligned, and mirrors real-world ETL pipelines in intelligence analysis. The context supplied to each agent is purposeful, structured, and intentionally small—enabling predictable reasoning and ensuring that the system behaves deterministically. 

### Further Enhancements
1. I would create a telegram bot that is interactive and can take date and channel input from the user to scrape public channels and produce output
2. Add memory service as a log to study how the LLM processes context from a large corpus of text, to write better system prompts for deduplication and category extraction
3. Use advanced spatial reasoning to geocode a particular location based on multiple location estimations of the same incident
4. Create multiple records out of a single chunk of texts that describes multi-geographic incidents
