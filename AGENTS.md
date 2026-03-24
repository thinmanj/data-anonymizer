# AGENTS.md

## Project Overview

**data-anonymizer** is a Python library for anonymizing sensitive data while preserving mathematical properties of monetary values. It uses affine transformation for monetary values and Faker for realistic PII generation.

- **Language**: Python 3.8+
- **Dependencies**: `numpy>=1.20.0`, `Faker>=18.0.0`
- **Source**: `src/data_anonymizer/`
- **Tests**: `tests/`
- **Examples**: `examples/`

---

## Build / Lint / Test Commands

### Install Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

### Run Tests

```bash
# Run all tests
python tests/test_anonymizer.py

# Run all tests with pytest
pytest tests/test_anonymizer.py -v

# Run all tests with coverage
pytest tests/test_anonymizer.py --cov=src/data_anonymizer --cov-report=term-missing

# Run a single test class
pytest tests/test_anonymizer.py::TestMonetaryTransformer -v

# Run a single test method
pytest tests/test_anonymizer.py::TestMonetaryTransformer::test_basic_transformation -v

# Run a specific test by name pattern
pytest tests/test_anonymizer.py -k "test_anonymize_name" -v
```

### Run Examples

```bash
python examples/example_usage.py
python examples/faker_example.py
python examples/csv_example.py
```

### Package Installation

```bash
pip install -e .
```

---

## Code Style Guidelines

### Formatting

- **Indentation**: 4 spaces (no tabs)
- **Line length**: ~88 chars max (follow PEP 8)
- **No trailing whitespace** on lines
- **One blank line** between top-level definitions (classes, functions)
- **Two blank lines** before class docstrings at module level
- **No blank line** at end of file

### Imports

Order imports as follows, separated by blank lines:

1. Standard library imports (`sys`, `hashlib`, `random`, `datetime`)
2. Third-party imports (`numpy`, `faker`)
3. Local imports (`from .anonymizer import ...`)

```python
import hashlib
import random
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

import numpy as np
from faker import Faker

from .anonymizer import DataAnonymizer, MonetaryTransformer
```

### Type Annotations

- Use `typing` module for complex types: `List`, `Dict`, `Optional`, `Union`, `Any`
- Use built-in generics where possible (Python 3.9+): `list[str]`, `dict[str, Any]`
- Use lowercase for type variable names

### Naming Conventions

| Element         | Convention   | Example                          |
|-----------------|--------------|----------------------------------|
| Classes         | PascalCase   | `DataAnonymizer`, `MonetaryTransformer` |
| Functions/methods | snake_case | `anonymize_name`, `get_params`   |
| Variables       | snake_case   | `fake_name`, `hash_val`, `anon_data` |
| Constants       | UPPER_SNAKE  | Not heavily used; follow snake_case otherwise |
| Private attrs   | `_snake_case` | `_name_cache`, `_address_cache` |
| Instance attrs  | snake_case   | `self.seed`, `self.locale`      |

### Docstrings

Use Google-style docstrings with `Args:`, `Returns:`, `Raises:` sections:

```python
def anonymize_name(self, name: str, consistent: bool = True) -> str:
    """
    Anonymize a person's name using Faker.

    Args:
        name: Original name.
        consistent: If True, same name always maps to the same anonymized name.

    Returns:
        Anonymized name.
    """
```

- Class docstrings describe purpose and key behavior
- Method docstrings document parameters and return values
- Keep docstrings concise; no docstring for trivial getters/setters

### Error Handling

- Use exceptions sparingly; prefer returning `None` or raising `ValueError` for invalid input
- Validate inputs at method entry points when critical
- Example pattern for type checking:

```python
if not isinstance(value, (tuple, list)):
    raise TypeError("value must be a tuple or list")
```

### Control Flow

- Use `isinstance()` for type checks, not `type()` comparisons
- Prefer `if/elif/elif/else` chains over nested dictionaries for dispatch
- Keep boolean expressions readable; break long lines at logical operators

### Class Structure

Follow this pattern:

```python
class ClassName:
    """One-line summary.

    Extended description if needed (2-3 sentences max).
    """

    def __init__(self, param: str = "default"):
        """Initialize the class."""
        self.param = param
        self._private_attr = {}

    def public_method(self) -> str:
        """One-line docstring."""
        return self.param
```

### Caching

- Use `_cache` attributes for consistent anonymization (e.g., `_name_cache`, `_address_cache`)
- Initialize caches in `__init__` as `{}`
- Check cache before generating new values; populate on miss

### Testing

- Place tests in `tests/test_anonymizer.py`
- Use `unittest.TestCase` with descriptive `test_` method names
- Use `assertAlmostEqual` for floating-point comparisons
- Use `assertIsInstance` for type checks
- `setUp()` method initializes shared fixtures per test class
- Each test should be self-contained and not depend on execution order

---

## Architecture Notes

### DateTimeTransformer

Applies offset transformation to date/time values. Supports:
- `transform(datetime)` — apply offset to datetime
- `transform_date(date)` — apply offset to date
- `get_params()` — return offset in days

Preserves chronological ordering and exact durations between dates.

### MonetaryTransformer

Applies affine transformation (`y = ax + b`) to monetary values. Supports:
- `transform(value)` — apply transformation
- `transform_array(values)` — batch transform
- `inverse_transform(value)` — reverse transformation
- `get_params()` — return scale and shift

### DataAnonymizer

Main class. Provides `anonymize_*` methods for each field type. Uses internal caches for consistency. Supports `locale` parameter (e.g., `en_US`, `es_ES`, `fr_FR`).

### Field Types (for `anonymize_dataset`)

| Type         | Method                   |
|--------------|--------------------------|
| `name`       | `anonymize_name`         |
| `address`    | `anonymize_address`      |
| `email`      | `anonymize_email`        |
| `phone`      | `anonymize_phone`        |
| `company`    | `anonymize_company`      |
| `ssn`        | `anonymize_ssn`          |
| `credit_card`| `anonymize_credit_card`  |
| `geolocation`| `anonymize_geolocation`  |
| `monetary`   | `anonymize_monetary`     |
| `date`       | `anonymize_date`         |
| `datetime`   | `anonymize_datetime`     |
| `timestamp`  | `anonymize_timestamp`    |

### Consistency

All `anonymize_*` methods accept a `consistent: bool = True` parameter. When `True`, the same input always produces the same output via hash-based seeding of the Faker instance. When `False`, each call produces a new random value.

---

## File Locations

| File                  | Purpose                        |
|-----------------------|--------------------------------|
| `src/data_anonymizer/__init__.py` | Package init, exports `DataAnonymizer`, `MonetaryTransformer`, `DateTimeTransformer` |
| `src/data_anonymizer/anonymizer.py` | Core implementation |
| `tests/test_anonymizer.py` | Unit tests (34 tests) |
| `examples/example_usage.py` | Basic usage demos |
| `examples/faker_example.py` | Faker and locale demos |
| `examples/csv_example.py` | CSV processing demo |
| `setup.py` | Package configuration |
| `requirements.txt` | Runtime dependencies |
