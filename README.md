# OpenAstrocytes Publication

**OpenAstrocytes: AI-ready dynamic activity from the astrocyte network**

This repository contains the code and analysis for the OpenAstrocytes publication, demonstrating how off-the-shelf vision transformer embeddings (DINOv3) capture rich structure in astrocyte calcium dynamics.

## Overview

This project combines:
- A **Python package** (`oa_pub`) with analysis utilities for working with astrocyte calcium imaging and embeddings
- A **Quarto document** that generates the full publication with embedded analysis, figures, and narrative

The analysis demonstrates that DINOv3 patch embeddings applied to astrocyte calcium imaging data can:
- Reflect astrocyte network anatomy
- Capture evoked dynamics in response to compound applications
- Generalize across distinct pharmacological profiles
- Enable accurate decoding of applied compounds from single patches

## Repository Structure

```
pub-open-astrocytes/
├── src/oa_pub/              # Python analysis package
│   ├── analysis/            # Data loading and statistical utilities
│   │   ├── _common.py      # Helper functions (e.g., is_between)
│   │   ├── _constants.py   # Constants (patch grid dimensions, compound aliases)
│   │   ├── _extraction.py  # Data loading (get_movie, get_movie_traces)
│   │   └── _stats.py       # Statistics (baseline_normalize, bootstrap)
│   └── figures/             # Plotting utilities
│       └── __init__.py     # Visualization functions
├── quarto/                  # Publication source
│   ├── index.qmd           # Main Quarto document with analysis
│   ├── _quarto.yml         # Quarto configuration
│   ├── _brand.yml          # Forecast branding
│   ├── img/                # Images and assets
│   └── csl/                # Citation styles
├── _public/                 # Generated publication output
├── pyproject.toml          # Python package configuration
└── README.md               # This file
```

## Prerequisites

- **Python 3.12** or later
- **uv** package manager ([installation instructions](https://github.com/astral-sh/uv))
- **Quarto** ([installation instructions](https://quarto.org/docs/get-started/))

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/forecast-bio/pub-open-astrocytes.git
cd pub-open-astrocytes
```

### 2. Set up Python environment

```bash
# Install dependencies with uv
uv sync

# This creates a virtual environment in .venv/ and installs all dependencies
```

### 3. Verify installation

```bash
# Test that the package is importable
uv run python -c "import oa_pub; print('Success!')"
```

## Reproducing the Publication

### Generate the full publication

```bash
cd quarto
uv run quarto render
```

This will:
- Execute all Python code blocks in `index.qmd`
- Load data from the OpenAstrocytes dataset
- Generate all figures and analyses
- Output the complete publication to `_public/index.html`

**Note:** The first render will take significant time as it streams data from the cloud and computes embeddings. Subsequent renders use Quarto's caching system for faster execution.

### Preview with live reload

```bash
cd quarto
uv run quarto preview
```

This opens a browser with the publication and automatically reloads when you make changes to `index.qmd`.

## Working with the Python Package

### Using the analysis utilities

```python
import oa_pub.analysis as analysis

# Load a recording by UUID
movie_uuid = "your-movie-uuid-here"
frames = analysis.get_movie(movie_uuid, verbose=True)

# Get patch embedding traces (14×14 grid)
traces = analysis.get_movie_traces(movie_uuid, verbose=True)

# Extract time information
times, dt = analysis.movie_times(frames)

# Apply baseline normalization
normalized, mean, std = analysis.baseline_normalize(
    times, signal, window=(-10, 0)
)

# Bootstrap statistics
boot_results = analysis.boot_stat(
    data,
    lambda x: np.mean(x, axis=0),
    n=200
)
```

### Using the plotting utilities

```python
from oa_pub.figures import plot_micrograph, plot_trace_grid
from forecast_style import HouseStyle

# Plot a micrograph with scale bar
with HouseStyle() as s:
    plot_micrograph(s, image, scale_bar=100.)

# Plot a grid of traces
with HouseStyle() as s:
    fig, axs = plt.subplots(14, 14, figsize=(12, 12))
    plot_trace_grid(axs, times, traces, color='b')
```

## Data Access

This project uses the OpenAstrocytes dataset, which is publicly available and streamed on-demand:

```bash
# Install the astrocytes package
pip install astrocytes

# Or with uv
uv add astrocytes
```

The `oa_pub.analysis` module handles data streaming automatically when you call functions like `get_movie()` and `get_movie_traces()`.

## Development

### Adding dependencies

```bash
# Add a runtime dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>
```

### Running tests

```bash
# Run any test scripts
uv run python -m pytest
```

### Code structure conventions

- Private modules use `_` prefix (e.g., `_extraction.py`)
- Public API is exposed through `__init__.py` files
- All functions include NumPy-style docstrings
- Use `verbose` parameters for progress output during data loading

## Citation

If you use this code or the OpenAstrocytes dataset in your research, please cite:

```bibtex
@article{openastrocytes2025,
  title={OpenAstrocytes: AI-ready dynamic activity from the astrocyte network},
  author={Levesque, Maxine and Poskanzer, Kira},
  year={2025}
}
```

## Links

- **OpenAstrocytes Dataset**: Available via the `astrocytes` Python package
- **Forecast Bio**: [https://forecast.bio](https://forecast.bio)
- **Publication**: [View the rendered publication](_public/index.html)

## License

This project is released under [LICENSE](LICENSE).

## Contact

For questions or issues:
- Open an issue on GitHub
- Email: maxine@forecast.bio
