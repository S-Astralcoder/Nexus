# Nexus

An agent building framework designed to simplify the creation of AI agents with pre-built, modular components.

## Features

- **Pre-built Components**: Modular building blocks for rapid agent assembly.
- **Type-safe & Extensible**: Built on top of Pydantic for validation and structured configurations.
- **Async-First Networking**: Native HTTP client support powered by HTTPX.

## Requirements

- Python >= 3.12

## Installation

Install using `uv`:

```bash
uv pip install -e .
```

Or with standard `pip`:

```bash
pip install -e .
```

## Quick Start

```python
import nexus

print(nexus.hello())
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](file:///C:/Users/blaze/WorkSpace/Project%20Workspace/Python%20Packages/Nexus%20V2/LICENSE) file for details.
