---
name: holographic-memory
description: "Set up and use Hermes Agent's holographic memory — SQLite fact store with FTS5 search, trust scoring, entity resolution, and Holographic Reduced Representations (HRR) for compositional retrieval."
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos]
metadata:
  hermes:
    tags: [memory, holographic, hrr, facts, plugin]
    related_skills: [hermes-agent]
---

# Holographic Memory Plugin

A **MemoryProvider** plugin for Hermes Agent that gives you structured fact storage with algebraic retrieval via Holographic Reduced Representations (HRR).

Docs: [plugins/memory/holographic/README.md](https://github.com/NousResearch/hermes-agent/blob/main/plugins/memory/holographic/README.md)

## Setup

```bash
# 1. Set the memory provider to holographic
hermes config set memory.provider holographic

# 2. Install numpy (optional but recommended — powers HRR algebra)
pip install numpy

# 3. Add plugin config to ~/.hermes/config.yaml under `plugins.hermes-memory-store:`
#    (manually or via python script — hermes config set doesn't handle nested plugin config)
```

### Plugin Config (`plugins.hermes-memory-store`)

| Key | Default | Description |
|-----|---------|-------------|
| `db_path` | `$HERMES_HOME/memory_store.db` | SQLite database path |
| `auto_extract` | `false` | Auto-extract facts at session end |
| `default_trust` | `0.5` | Default trust score for new facts |
| `hrr_dim` | `1024` | HRR vector dimensions |
| `min_trust_threshold` | `0.3` | Minimum trust for retrieval results |
| `hrr_weight` | `0.3` | Weight given to HRR similarity in hybrid search |
| `temporal_decay_half_life` | `0` | Days for trust decay (0 = disabled) |

Example config block:
```yaml
plugins:
  hermes-memory-store:
    db_path: $HERMES_HOME/memory_store.db
    auto_extract: true
    default_trust: 0.5
    hrr_dim: 1024
    min_trust_threshold: 0.3
```

### Requirements

- **None for base** — SQLite is always available
- **numpy** (optional) — enables HRR vectors, probe/related/reason/contradict actions. Without it, falls back to FTS5 + Jaccard similarity only.

## Tools Provided

Once loaded (new session / `/reset`), these tools appear:

### `fact_store` — 9 actions

| Action | Description |
|--------|-------------|
| `add` | Store a fact with content, category, tags |
| `search` | FTS5 + Jaccard + HRR hybrid keyword lookup |
| `probe` | Entity recall: ALL facts about a person/thing |
| `related` | What connects to an entity? Structural adjacency |
| `reason` | Compositional: facts connected to MULTIPLE entities simultaneously |
| `contradict` | Memory hygiene: find conflicting claims |
| `update` | Update a fact's content/trust/tags/category |
| `remove` | Delete a fact by ID |
| `list` | Browse facts, optionally filtered by category |

### `fact_feedback` — 2 actions

| Action | Description |
|--------|-------------|
| `helpful` | Mark fact as helpful (trust += 0.05) |
| `unhelpful` | Mark fact as unhelpful (trust -= 0.10) |

## How HRR Works (briefly)

- Each concept is a **phase vector** (angles in [0, 2π)) of 1024 dimensions
- **bind** = phase addition (associates two concepts)
- **unbind** = phase subtraction (retrieves a bound concept)
- **bundle** = circular mean (merges multiple concepts)
- This enables algebraic queries like "find facts about X AND Y" via vector operations

Atoms are generated deterministically from SHA-256 — same across processes/machines.

## Usage Tips

- Proactively `fact_store(action='add')` facts about people, projects, preferences
- Before answering user questions, `fact_store(action='probe', entity='...')` or `fact_store(action='reason', entities=[...])` first
- Use `fact_feedback` after using a fact — trains trust scores over time
- The `auto_extract: true` option auto-detects user preferences and project decisions at session end
- `fact_store(action='contradict', limit=10)` finds conflicting facts for periodic memory hygiene

## Troubleshooting

- **Tools not appearing**: `/reset` for a new session
- **HRR operations silently falling back**: Check `numpy` is installed (`python3 -c "import numpy"`)
- **Config changes not taking effect**: Stop and restart the CLI or gateway
- **Duplicate facts ignored**: The store deduplicates by content (UNIQUE constraint on content column)
