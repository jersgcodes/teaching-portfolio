"""Content-core aggregator.

Merges `projects.yaml` (canonical) with light auto-decoration from each
project's `~/claude/<slug>/` directory. Outputs `data/projects.json` for the
consumer sites to render.

See `docs/spikes/aggregator-extraction.md` for the design rationale.
"""

__version__ = "0.1.0"
