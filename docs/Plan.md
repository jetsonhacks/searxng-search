# Plan

## Milestone 1
Install and uninstall SearXNG

### Deliverables
- `tools/searxng/install-searxng.sh`
- `tools/searxng/uninstall-searxng.sh`

### Validation
- Installer completes successfully on a clean system
- SearXNG starts and responds locally
- Uninstaller removes the installed components cleanly

## Milestone 2
Demonstrate SearXNG search from Python

### Deliverables
- `tools/searxng/search_searxng.py`

### Validation
- Python script performs a query successfully
- Script handles endpoint errors clearly
- Script prints a small normalized result set

## Milestone 3
Expose search through MCP

### Deliverables
- `tools/searxng/mcp_server.py`

### Validation
- MCP tool can be started locally
- Tool exposes a search action with a clear schema
- Tool returns structured search results

## Milestone 4
Integrate with OpenClaw

### Deliverables
- Example integration under `examples/` or repository docs

### Validation
- OpenClaw can use the search capability in a controlled example
- Integration steps are documented clearly

## Milestone 5
Add the OpenClaw skill

### Deliverables
- `skills/searxng-search/SKILL.md`

### Validation
- Skill describes when and how to use search
- Skill remains concise and specific
- Skill matches the implemented tool behavior

## Milestone 6
Refine tests and documentation

### Deliverables
- Expanded docs
- Smoke tests or lightweight checks
- Cleanup of repository structure as needed

### Validation
- Repository is understandable end to end
- Documentation matches the code
- A new reader can follow the intended workflow