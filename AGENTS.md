# AGENTS.md

## Cursor Cloud specific instructions

### Overview

DeepPhrase is a Python framework for generating intent-based query phrases using neural representations. It fetches data from social channels (Twitter, Reddit, News), applies clustering (KMeans, LDA) with word embeddings (GloVe, FastText, Word2Vec, Universal Sentence Encoder), and iteratively refines search query phrases. See `README.md` for full architecture and usage details.

### Python version

This project requires **Python 3.8** due to old dependency version constraints. A virtual environment is created at `/workspace/.venv` using `python3.8`. Always activate it before running any Python commands:

```
source /workspace/.venv/bin/activate
```

The `requirements.txt` pins very old versions. The following version adjustments are needed for a working environment:
- `scikit-learn==0.22.2.post1` (not 1.5.0; code uses `calinski_harabaz_score` removed in sklearn 0.23)
- `gensim==3.8.3` (not 3.4.0; 3.4.0 fails to build, 3.8.3 is the last 3.x with `gensim.summarization`)
- `numpy==1.21.6` (not 1.22.0; sklearn 0.22 + numpy 1.22 triggers `np.float` removal error)
- `tensorflow==2.11.1` (not 2.12.1; TF 2.12 requires numpy >= 1.22)
- `tensorflow_hub==0.13.0` (not 0.2.0; old version has protobuf incompatibility)
- `pymagnitude` latest (not 0.1.120; old version times out building from source)
- `matplotlib` latest 3.7.x (not 2.2.2; old version unavailable for Python 3.8)
- `pandas==1.5.3` (pyLDAvis 2.1.2 is incompatible with pandas 2.x)
- `sentencepiece` latest (not 0.1.8; exact version unavailable)
- `nltk` must be installed separately (not in requirements.txt but used by `features/preprocess.py`)

### Running the project

The core entry point is `seedcontext/seed_augment.py::generate_iterative_seed()`. The `examples/all_permutations.py` script runs all combinations. Both require:

1. **API keys** configured in `config/keys.py` (Twitter, Reddit, and/or News API)
2. **Pre-trained `.magnitude` model files** in a `models/` directory (GloVe, FastText, Word2Vec)
3. **A storage backend**: MongoDB (default), Redis, or Kafka

Without API keys and model files, you can still test the core ML pipeline locally (preprocessing, clustering, LDA topic modeling) using synthetic data.

### Lint

No linter is configured in the project. Run `flake8 --exclude=.venv .` for basic checks.

### Log file path

`constants/modelconstants.py` has `LOG_FILE_PATH` hardcoded to a Windows path. The logging module (`commonutils/logutils.py`) uses this path. For local testing, the path will fail on Linux but doesn't block non-logging code paths.
