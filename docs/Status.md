# Status

## Current State

Milestone 1 complete.

## What Was Completed

- Added `tools/searxng/install-searxng.sh`
- Added `tools/searxng/uninstall-searxng.sh`
- Validated install and uninstall cycle locally
- Confirmed SearXNG served JSON search results successfully

## Validation Notes

- Initial install on port 8080 conflicted with NemoClaw
- Installing on port 8081 succeeded
- Uninstall removed the local container, generated files, and image cleanly
- Re-running uninstall completed cleanly when resources were already absent

## Current Focus

Prepare for Milestone 2: demonstrate SearXNG search from Python.

## Next Step

Implement `tools/searxng/search_searxng.py`
