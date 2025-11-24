# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a publication codebase for **OpenAstrocytes**: AI-ready dynamic activity from the astrocyte network. The project combines scientific analysis code with Quarto-based publication generation.

## Technology Stack

- **Python 3.12** (managed via `uv` package manager)
- **Quarto** for scientific publication rendering (qmd → HTML)
- **Key dependencies**: `astrocytes`, `atdata`, `toile`, `forecast-style`, `numpy`, `matplotlib`, `modal`, `jupyter`

## Development Commands

### Package Management (via uv)

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Run Python with the virtual environment
uv run python <script>

# Run the embed script (defined in pyproject.toml)
uv run embed
```

The virtual environment is in `.venv/` and Python 3.12 is specified in `.python-version`.

### Building the Publication

```bash
# Render the Quarto document
cd quarto
quarto render

# Preview with live reload
cd quarto
quarto preview

# The output goes to _public/ directory at repo root
```

The main publication document is `quarto/index.qmd`, which generates `_public/index.html`.

## Code Architecture

### Module Structure

```
src/oa_pub/
├── analysis/           # Data analysis utilities
│   ├── _common.py     # Helper functions (e.g., is_between)
│   ├── _constants.py  # Constants (N_PATCHES_X, N_PATCHES_Y, COMPOUND_ALIASES)
│   ├── _extraction.py # Data extraction (get_movie, get_movie_traces, movie_times)
│   └── _stats.py      # Statistical utilities (baseline_normalize, boot_traces, boot_stat)
└── figures/            # Plotting and visualization
    └── __init__.py    # Micrograph and trace plotting (plot_micrograph, plot_trace_grid, plot_trajectory_3d)
```

### Key Concepts

**Data Sources**:
- The codebase works with two primary data types:
  - `BathApplicationFrame`: Individual frames from astrocyte calcium imaging recordings
  - `PatchEmbeddingTrace`: Patch-level embeddings from vision transformer (DINOv3) applied to recordings
- Data is streamed via `atdata` and `astrocytes` packages from cloud storage (WebDataset format)

**Spatial Organization**:
- Vision embeddings are organized as 14×14 patch grids (N_PATCHES_X, N_PATCHES_Y)
- Each recording (identified by `movie_uuid`) has multiple frames and corresponding patch traces
- Patch traces are spatially indexed via `i_patch` and `j_patch` coordinates

**Analysis Pattern**:
1. Extract movie frames or traces by `movie_uuid`
2. Apply baseline normalization using pre-stimulus window
3. Perform bootstrap resampling for statistical analysis
4. Visualize with custom plotting utilities

### External Dependencies

- `forecast_style.HouseStyle`: Custom plotting style from forecast-bio/style repo (Git dependency)
- `astrocytes.data.bath_application`: Backend manifest for accessing astrocyte calcium imaging data
- `atdata.Dataset`: Streaming dataset interface for WebDatasets

## Common Patterns

**Filtering by time window**:
```python
from oa_pub.analysis import is_between
filter_mask = is_between(times, window=(-10, 0))
```

**Loading a recording**:
```python
from oa_pub.analysis import get_movie, get_movie_traces, movie_times

frames = get_movie(movie_uuid="...")
traces = get_movie_traces(movie_uuid="...")  # Returns 14×14 grid
times, dt = movie_times(frames)
```

**Bootstrap statistics**:
```python
from oa_pub.analysis import boot_stat

boot_results = boot_stat(data, lambda x: np.mean(x, axis=0), n=200)
```

## Known Issues

- There's a metadata timing bug in the `toile` export from bath application data (see `movie_times` function in `_extraction.py`)
- Trace classes lack full typing support (see issue #15 in forecast-bio/open-astrocytes)
- Compound name typos exist in raw metadata (handled via `COMPOUND_ALIASES` dict)

## Branch Strategy

- Current branch: `release/v1.2.0`
- Main branch: `main` (use for PRs)
- The repo appears to use feature branches with personal develop branches (e.g., `develop/maxine`)
