# Data Anonymizer

A Python library for anonymizing sensitive data while preserving mathematical properties of monetary values.

## Features

- **Name Anonymization**: Consistent mapping using Faker library for realistic, diverse names
- **Address Anonymization**: Generate realistic fake addresses with high diversity
- **Email Anonymization**: Hash-based email anonymization
- **Phone Number Anonymization**: Locale-appropriate phone numbers using Faker
- **Company Name Anonymization**: Generate realistic company names
- **SSN Anonymization**: Generate valid Social Security Numbers
- **Credit Card Anonymization**: Generate Luhn-valid credit card numbers
- **Geolocation Anonymization**: Add controlled noise to GPS coordinates
- **Monetary Value Transformation**: Uses affine transformation (y = ax + b) to preserve mathematical properties
- **Multi-Locale Support**: Generate data appropriate for different regions (US, Spanish, French, German, Japanese, etc.)

## Why Affine Transformation for Monetary Values?

The library uses affine transformation for monetary values, which has important properties:

- **Preserves differences**: If A - B = $100 in original data, the difference between transformed A' and B' will be scaled by the same factor
- **Preserves relative magnitudes**: The ordering and relative sizes are maintained
- **Enables analysis**: Statistical operations like sum, mean, and variance can be performed on transformed data and results can be mapped back
- **Linear operations preserved**: Operations like `sum(values)` maintain their mathematical relationships

This is similar to projecting data into a different coordinate system where the structure is preserved but the actual values are obscured.

## Installation

```bash
cd data-anonymizer
pip install -r requirements.txt
```

Or install dependencies directly:
```bash
pip install numpy Faker
```

## Quick Start

```python
from data_anonymizer import DataAnonymizer

# Create an anonymizer with a seed for reproducibility
# Specify locale for region-appropriate data generation
anonymizer = DataAnonymizer(seed=42, locale='en_US')

# Anonymize individual values
anon_name = anonymizer.anonymize_name("John Smith")
anon_address = anonymizer.anonymize_address("123 Main Street")
anon_company = anonymizer.anonymize_company("Acme Corp")
anon_ssn = anonymizer.anonymize_ssn("123-45-6789")
anon_card = anonymizer.anonymize_credit_card("4532-1234-5678-9010")
anon_amount = anonymizer.anonymize_monetary(1000.00)
anon_lat, anon_lon = anonymizer.anonymize_geolocation(40.7128, -74.0060)

# Anonymize a complete dataset
data = [
    {
        "name": "Alice Johnson",
        "email": "alice@email.com",
        "address": "456 Oak Avenue",
        "location": {"latitude": 34.0522, "longitude": -118.2437},
        "balance": 1500.00
    }
]

field_types = {
    "name": "name",
    "email": "email",
    "address": "address",
    "location": "geolocation",
    "balance": "monetary"
}

anonymized_data = anonymizer.anonymize_dataset(data, field_types)
```

## Mathematical Properties Example

```python
from data_anonymizer import DataAnonymizer

anonymizer = DataAnonymizer(seed=42)

# Original transactions
transactions = [100.0, 200.0, 300.0, 400.0, 500.0]

# Anonymize
anon_transactions = [anonymizer.anonymize_monetary(t) for t in transactions]

# Properties preserved:
# 1. Sum structure: sum(anon) = scale * sum(original) + n * shift
# 2. Mean structure: mean(anon) = scale * mean(original) + shift
# 3. Ratios approximately preserved for large values
# 4. Differences scaled by the same factor
```

## Multi-Locale Support

```python
# Generate Spanish names and addresses
anonymizer_es = DataAnonymizer(seed=42, locale='es_ES')
print(anonymizer_es.anonymize_name("John Smith"))  # e.g., "Felipe Téllez"

# Generate French data
anonymizer_fr = DataAnonymizer(seed=42, locale='fr_FR')
print(anonymizer_fr.anonymize_address("123 Main St"))  # e.g., "rue Louis"

# Supported locales: en_US, es_ES, fr_FR, de_DE, ja_JP, and many more
```

## Usage Examples

See the example files for comprehensive demonstrations:

```bash
cd examples
python example_usage.py      # Basic examples
python faker_example.py      # Faker features and locales
python csv_example.py        # CSV file processing
```

## Running Tests

```bash
cd tests
python test_anonymizer.py
```

## API Reference

### DataAnonymizer

Main class for data anonymization.

#### Constructor

- `DataAnonymizer(seed: int = None, locale: str = 'en_US')`: Initialize anonymizer with optional seed and locale

#### Methods

- `anonymize_name(name: str, consistent: bool = True) -> str`: Anonymize a person's name
- `anonymize_address(address: str, consistent: bool = True) -> str`: Anonymize a street address
- `anonymize_email(email: str, consistent: bool = True) -> str`: Anonymize an email address
- `anonymize_phone(phone: str, consistent: bool = True) -> str`: Anonymize a phone number
- `anonymize_company(company: str, consistent: bool = True) -> str`: Anonymize a company name
- `anonymize_ssn(ssn: str, consistent: bool = True) -> str`: Anonymize a Social Security Number
- `anonymize_credit_card(card: str, consistent: bool = True) -> str`: Anonymize a credit card number (Luhn-valid)
- `anonymize_geolocation(latitude: float, longitude: float, noise_radius_km: float = 10.0) -> tuple`: Anonymize GPS coordinates
- `anonymize_monetary(value: float) -> float`: Anonymize a monetary value
- `anonymize_dataset(data: List[Dict], field_types: Dict[str, str], **kwargs) -> List[Dict]`: Anonymize an entire dataset

### MonetaryTransformer

Specialized class for monetary value transformation using affine transformation.

#### Methods

- `transform(value: float) -> float`: Apply transformation to a single value
- `transform_array(values: List[float]) -> List[float]`: Transform a list of values
- `inverse_transform(value: float) -> float`: Reverse the transformation
- `get_params() -> Dict[str, float]`: Get the transformation parameters (scale and shift)

## Field Types

When using `anonymize_dataset()`, specify field types:

- `"name"`: Person's name
- `"address"`: Street address
- `"email"`: Email address
- `"phone"`: Phone number
- `"company"`: Company name
- `"ssn"`: Social Security Number
- `"credit_card"`: Credit card number
- `"geolocation"`: GPS coordinates (supports tuple, list, or dict format)
- `"monetary"`: Monetary values

## Consistency

By default, the library maintains consistency: the same input always maps to the same output. This is crucial for:

- Maintaining relationships in the data (e.g., same person appears multiple times)
- Reproducible anonymization
- Testing and validation

Set `consistent=False` for methods that support it to get different outputs each time.

## Use Cases

- **Data Sharing**: Anonymize production data for development/testing environments
- **Analytics**: Preserve statistical properties while protecting sensitive information
- **Compliance**: Meet privacy requirements (GDPR, CCPA) while maintaining data utility
- **Research**: Share datasets for research purposes without exposing PII

## What's New in Latest Version

### Faker Integration (v0.2.0)
- **Massive diversity improvement**: Previously limited to 182 name combinations (14 × 13), now generates millions of unique, realistic names
- **Multi-locale support**: Generate region-appropriate data for 50+ locales
- **New field types**: Company names, SSN, and Luhn-valid credit card numbers
- **More realistic data**: Addresses, phone numbers, and names match real-world patterns
- **21 unit tests**: Increased from 13 tests with comprehensive coverage

## Limitations

- Affine transformation doesn't preserve exact ratios (though they're approximately preserved for large values)
- Geolocation anonymization uses simple Euclidean distance (not geodesic)
- SSN generation is US-centric (use appropriate locale for other regions)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
