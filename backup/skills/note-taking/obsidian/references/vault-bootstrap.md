# Vault Bootstrap

> Reference: bootstrapping a new Hermes + Obsidian vault from a guide document.
> Based on a real setup, June 2026.

## When to Bootstrap

User shares a vault guide doc (or just says "oku kur" / "set it up") and wants a full vault created from scratch:

1. Check if vault path exists (`OBSIDIAN_VAULT_PATH` or `~/vault` or `~/Documents/Obsidian Vault`)
2. If missing, create the full skeleton (see below)
3. Create AGENTS.md — the critical file with operating rules
4. Create all `index.md` files
5. Create 3 identity notes (contact, agent, machine)
6. Set `OBSIDIAN_VAULT_PATH` in `~/.hermes/.env`
7. Init git + auto-commit cron job
8. Optionally set up Syncthing for cross-device sync (see below)

## Skeleton

```
vault/
  index.md
  AGENTS.md

  Inbox/
    index.md
  Journal/
    index.md
  Projects/
    index.md
  Areas/
    index.md
  Resources/
    index.md
  Archive/
    index.md

  Directory/
    index.md
    contacts/index.md
    companies/index.md
    agents/index.md
    machines/index.md
    repos/index.md

  Wiki/
    index.md
```

**Do not create more folders upfront.** The structure grows with use.

## AGENTS.md Essentials

The centerpiece. Must cover:

- **Destination rules** — which vault section holds what
- **Operating rules** — read AGENTS.md + index.md first; update index in the same pass as any file change; keep memory short; never invent facts
- **Trail rule** — at end of meaningful work, leave what changed, where, and next action

## Identity Notes (Day One)

Create these three immediately:

| Note | Template |
|---|---|
| `Directory/contacts/[owner].md` | Role, priorities, communication style, preferences, do-nots, active projects |
| `Directory/agents/[agent-name].md` | Role, provider/model, key config, rules |
| `Directory/machines/[hostname].md` | Hostname, IP, OS, services, connection notes |

## Git Setup

```bash
cd ~/vault
git init
git config user.name "Owner Name"
git config user.email "owner@email"
```

**.gitignore:**
```
.obsidian/workspace*
.trash/
.stfolder*
.DS_Store
Thumbs.db
```

### Auto-commit cron

Create `auto-commit.sh`:
```bash
#!/bin/bash
VAULT="/path/to/vault"
cd "$VAULT" || exit 1
if [[ -z $(git status --porcelain) ]]; then exit 0; fi
git add -A
git commit -m "Auto-commit: $(date '+%Y-%m-%d %H:%M')" >/dev/null 2>&1
```

Schedule with cronjob tool: `schedule="0 18 * * *"`, `workdir=/path/to/vault`.

## OBSIDIAN_VAULT_PATH

Add to `~/.hermes/.env`:
```
OBSIDIAN_VAULT_PATH=/path/to/vault
```

## Syncthing Setup (Optional, Cross-Device Sync)

Install and start Syncthing:

```bash
sudo apt install -y syncthing
systemctl --user enable --now syncthing
```

Syncthing config lives at `~/.local/state/syncthing/config.xml` (Ubuntu 24.04) or `~/.config/syncthing/config.xml` (older). The GUI is at `http://localhost:8384`.

### Add Vault Folder

Edit `config.xml` directly (the REST API PUT returns 405 for folder creation). Add a `<folder>` block after the default folder, then restart:

```bash
pkill -x syncthing && sleep 2  # systemd auto-restarts
```

The device ID is available from the GUI or REST at `http://localhost:8384/rest/system/status`:

```bash
curl -s -H 'X-API-Key: APIKEY' http://localhost:8384/rest/system/status | python3 -c "import sys,json;print(json.load(sys.stdin)['myID'])"
```

### Connect Phone/Laptop

1. Install Syncthing app on phone
2. Add Remote Device using the server's device ID
3. The server sees the incoming connection request — approve it
4. Create a folder on the phone, share it with the server device
5. The server receives a folder share request — accept it, path=`/home/ubuntu/vault`

### Verify Sync

```bash
curl -s -H 'X-API-Key: APIKEY' http://localhost:8384/rest/db/status?folder=hermes-vault
```

Expected: `state: idle`, `needBytes: 0`.

## TL;DR Checklist

- [ ] Create skeleton directories
- [ ] Write AGENTS.md
- [ ] Write all index.md files (each folder)
- [ ] Create 3 identity notes (contact, agent, machine)
- [ ] Set `OBSIDIAN_VAULT_PATH` in `.env`
- [ ] `git init` + first commit
- [ ] Schedule auto-commit cron
- [ ] (Optional) Install Syncthing, add folder, connect devices
- [ ] Update relevant Area/Project index notes to link to new identity notes
