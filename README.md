# Jupyter AI Tabby Provider

`jupyter-ai-tabby` is an extension for Jupyter AI that registers [Tabby](https://www.tabbyml.com/) as a provider for code completions. This allows you to use your own self-hosted Tabby server for code generation within the Jupyter environment.

## Requirements

- Python 3.9+
- JupyterLab 4+
- `jupyter-ai-magics>=2.10.0,<3`

## Installation

### For Users

You can install the extension directly from GitHub using pip:

```bash
pip install git+https://github.com/qztseng/jupyter-ai-tabby.git
```

### For Developers

If you have cloned this repository locally and want to install it with your local modifications, you can do so in "editable" mode:

```bash
pip install -e .
```

## Configuration

After installation, you will need to configure the Tabby provider in Jupyter AI.

1.  Open JupyterLab.
2.  Open the Jupyter AI chat panel and go to the settings.
3.  Select "Tabby" from the list of completion models.
4.  The following configuration fields will be displayed:
    *   **URL**: The URL of your Tabby server's completion endpoint (e.g., `http://localhost:8080/v1/completions`).
    *   **API Key**: Your Tabby server API key. This is also read from the `TABBY_API_KEY` environment variable.
    *   **Prefix Context Length**: The maximum number of lines to use as context from the cells *before* the current cursor position.
    *   **Suffix Context Length**: The maximum number of lines to use as context from the cells *after* the current cursor position.

## Usage

Once configured, you can use Tabby for code completions in your Jupyter notebooks. Simply start typing in a code cell, and the completions from your Tabby server will appear automatically.

## Uninstallation

To remove the extension, execute:

```bash
pip uninstall jupyter-ai-tabby
```
