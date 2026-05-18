# WTD — Product Spec v1

## Overview

WTD ("What To Do?") is a platform for discovering local events — concerts, shows, parties, and more. The core value proposition is aggregation: a user arriving in a new city can open WTD and immediately see what's happening tonight without knowing any local venues, ticket sites, or promoters.

**v1 scope:** single city, admin-managed event ingestion, calendar/filter UI (interface TBD).

---

## Canonical Event Schema

Every source must produce an event conforming to this schema. This is the single source of truth across all agents.

| Field | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | |
| `description` | string | no | |
| `category` | enum | yes | `concert`, `theater`, `party`, `festival`, `sport`, `exhibition`, `other` |
| `start_datetime` | datetime (UTC) | yes | |
| `end_datetime` | datetime (UTC) | no | |
| `venue_name` | string | yes | |
| `venue_address` | string | no | |
| `city` | string | yes | |
| `is_free` | boolean | yes | Whether the event is free to attend |
| `price_info` | string | no | Human-readable price hint, e.g. "From €15", "€10–€30". Only relevant when `is_free` is false |
| `ticket_url` | url | no | Always the source of truth for pricing and availability |
| `image_url` | url | no | |
| `source_type` | enum | yes | `manual`, `api`, `scraper` |
| `source_url` | url | no | URL of the original listing |
| `source_connector_id` | fk | yes | Which connector produced this event |
| `external_id` | string | no | ID from the source system, used for deduplication |
| `status` | enum | yes | `draft`, `published`, `rejected` |
| `confirmed` | boolean | yes | Whether the event has been verified by a trusted user. Defaults to false |
| `confirmed_by` | fk (User) | no | The internal user who confirmed the event |
| `confirmed_at` | datetime | no | When the confirmation was made |

---

## Confirmation Model

Events can be "confirmed" by a trusted user to signal that the information has been verified as accurate. This is distinct from publishing — an event can be published but unconfirmed.

**v1 (internal users only):**
- Only logged-in internal/admin users can confirm events
- Confirmation sets `confirmed: true`, `confirmed_by`, and `confirmed_at`
- An event can be unconfirmed (flag reset) if information turns out to be wrong
- Confirmed status is visible to end users as a trust signal (e.g. a "verified" badge)

**v2 (future — public users):**
- Any registered user can confirm an event
- Confirmation becomes a many-to-many relationship (Event ↔ User)
- Threshold-based: e.g. 3+ confirmations marks an event as verified
- The `confirmed` boolean on the event model becomes a derived field

The v1 data model is designed so this migration doesn't require dropping columns — only adding a new join table.

---

## Agent Architecture

Each source type is handled by a dedicated agent. All agents share a common interface: they receive a connector config and return a list of canonical events.

### Common Agent Interface

```
Agent.run(connector: Connector) -> list[Event]
```

Agents are responsible for:
1. Fetching raw data from the source
2. Normalizing it into the canonical event schema
3. Deduplicating against existing events (by `external_id` or title + date + venue)
4. Returning events in the appropriate status for the pipeline to handle

Agents do NOT persist to the database directly — they return data and the pipeline handles persistence and moderation.

---

### Manual Agent

The simplest case — a human fills in a form in the admin interface.

- No automation
- Events created via the form go directly to `published` status (admin is trusted)
- Form must cover all required fields with sensible defaults and validation
- Supports image upload for `image_url`

---

### API Agent

Connects to structured event APIs (e.g. Ticketmaster, Eventbrite).

**Connector config:**
- `api_type`: identifier for which API (e.g. `ticketmaster`)
- `api_key`: credentials
- `city`: city to query
- `categories`: list of event categories to fetch
- `schedule`: cron expression for how often to run

**Behavior:**
- Authenticates with the API
- Fetches events matching the city and category filters
- Maps API response fields to the canonical schema, including `is_free` and `price_info`
- Uses `external_id` (the API's native event ID) for deduplication
- Events from trusted APIs are auto-published (`status: published`)
- Each API type has its own mapper class (e.g. `TicketmasterMapper`)

---

### Scraper Agent

Handles listing sites that don't have an API (e.g. Secret New York, Resident Advisor city pages).

**Connector config:**
- `url`: the page to scrape
- `city`: city this source covers
- `css_selectors` (optional): hints for extraction — `event_container`, `title`, `date`, `venue`, `price`, etc.
- `schedule`: cron expression

**Behavior:**
1. Fetches the page HTML
2. If `css_selectors` are configured, attempts extraction using them first
3. If CSS extraction fails or is not configured, falls back to LLM extraction:
   - Sends the page HTML (or a cleaned text version) to an LLM with a structured extraction prompt
   - LLM returns a list of events conforming to the canonical schema
4. Deduplicates by title + date + venue
5. Events from scrapers go to `draft` status and require admin review before publishing

**LLM extraction prompt contract:**
The prompt instructs the LLM to return a JSON array of events matching the canonical schema. The LLM is given the city and current date as context to resolve relative dates (e.g. "this Friday"). For price, the LLM should extract a short human-readable string (e.g. "From €10") or set `is_free: true` — never invent specific prices.

---

## Ingestion Pipeline

The orchestrator manages connector scheduling and routes agent output through the moderation layer.

```
Orchestrator
  └── triggers Agent.run(connector) on schedule
        └── Agent returns list[Event]
              └── Pipeline:
                    1. Deduplicate against DB
                    2. Persist new events (status per source type)
                    3. Notify admin of new drafts (if any)
```

**Deduplication logic:**
- If `external_id` + `source_connector_id` match an existing event → skip
- If title + `start_datetime` + `venue_name` match → skip
- Otherwise → insert as new event

**Error handling:**
- Agent failures are logged with connector ID, timestamp, and error
- A connector that fails N consecutive times is automatically paused and flagged in the admin

---

## Admin Interface

### Event Management
- List view: all events with filters by status, category, date range, source, is_free, confirmed
- Create/edit form (manual agent): all canonical fields, image upload
- Moderation queue: list of `draft` events from scrapers with approve/reject actions
- Bulk approve/reject in moderation queue
- Confirm/unconfirm action available on any published event

### Connector Management
- List of configured connectors with status (active, paused, last run, last error)
- Create/edit connector: type selection drives which config fields appear
- Manual trigger: run a connector on demand without waiting for the schedule
- Pause/resume connector

---

## Out of Scope for v1

- Multi-city support (city is a config value, not a user-facing filter)
- Public-facing UI (calendar, chatbot) — spec TBD
- Instagram / OCR agent
- Public user accounts or self-service event creation
- Public event confirmation (many-to-many model) — see v2 notes in Confirmation Model
- Duplicate merging UI (only auto-dedup on ingest)
