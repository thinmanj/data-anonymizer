"""
Example usage of the data anonymization library.
"""
import sys
sys.path.insert(0, '../src')

from data_anonymizer import DataAnonymizer
import json


def example_basic_anonymization():
    """Demonstrate basic anonymization of individual fields."""
    print("=== Basic Anonymization ===\n")
    
    anonymizer = DataAnonymizer(seed=42)
    
    # Anonymize name
    original_name = "John Smith"
    anon_name = anonymizer.anonymize_name(original_name)
    print(f"Name: {original_name} → {anon_name}")
    
    # Anonymize address
    original_address = "123 Main Street"
    anon_address = anonymizer.anonymize_address(original_address)
    print(f"Address: {original_address} → {anon_address}")
    
    # Anonymize geolocation
    original_lat, original_lon = 40.7128, -74.0060  # New York City
    anon_lat, anon_lon = anonymizer.anonymize_geolocation(
        original_lat, original_lon, noise_radius_km=5
    )
    print(f"Location: ({original_lat}, {original_lon}) → ({anon_lat:.4f}, {anon_lon:.4f})")
    
    # Anonymize monetary value
    original_amount = 1000.00
    anon_amount = anonymizer.anonymize_monetary(original_amount)
    print(f"Amount: ${original_amount:.2f} → ${anon_amount:.2f}")
    
    # Anonymize email
    original_email = "john.smith@company.com"
    anon_email = anonymizer.anonymize_email(original_email)
    print(f"Email: {original_email} → {anon_email}")
    
    # Anonymize phone
    original_phone = "(555) 123-4567"
    anon_phone = anonymizer.anonymize_phone(original_phone)
    print(f"Phone: {original_phone} → {anon_phone}")
    print()


def example_monetary_preservation():
    """Demonstrate that monetary operations preserve their characteristics."""
    print("=== Monetary Transformation Properties ===\n")
    
    anonymizer = DataAnonymizer(seed=42)
    
    # Original transactions
    transactions = [100.0, 200.0, 300.0, 400.0, 500.0]
    print(f"Original transactions: {transactions}")
    
    # Anonymize transactions
    anon_transactions = [anonymizer.anonymize_monetary(t) for t in transactions]
    print(f"Anonymized transactions: {[f'{t:.2f}' for t in anon_transactions]}")
    
    # Show that mathematical properties are preserved
    original_sum = sum(transactions)
    anon_sum = sum(anon_transactions)
    print(f"\nOriginal sum: ${original_sum:.2f}")
    print(f"Anonymized sum: ${anon_sum:.2f}")
    
    original_mean = original_sum / len(transactions)
    anon_mean = anon_sum / len(anon_transactions)
    print(f"\nOriginal mean: ${original_mean:.2f}")
    print(f"Anonymized mean: ${anon_mean:.2f}")
    
    # Ratios are preserved
    ratio_original = transactions[4] / transactions[0]
    ratio_anon = anon_transactions[4] / anon_transactions[0]
    print(f"\nRatio (last/first) original: {ratio_original:.4f}")
    print(f"Ratio (last/first) anonymized: {ratio_anon:.4f}")
    print(f"Ratios match: {abs(ratio_original - ratio_anon) < 0.0001}")
    
    # Differences are scaled
    diff_original = transactions[2] - transactions[1]
    diff_anon = anon_transactions[2] - anon_transactions[1]
    params = anonymizer.monetary_transformer.get_params()
    expected_diff = diff_original * params['scale']
    print(f"\nOriginal difference (3rd - 2nd): ${diff_original:.2f}")
    print(f"Anonymized difference: ${diff_anon:.2f}")
    print(f"Expected difference (scaled): ${expected_diff:.2f}")
    print(f"Differences match: {abs(diff_anon - expected_diff) < 0.01}")
    print()


def example_dataset_anonymization():
    """Demonstrate anonymizing a complete dataset."""
    print("=== Dataset Anonymization ===\n")
    
    # Sample customer dataset
    customers = [
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice@email.com",
            "phone": "(555) 111-2222",
            "address": "456 Oak Avenue",
            "location": {"latitude": 34.0522, "longitude": -118.2437},  # Los Angeles
            "balance": 1500.00,
            "last_purchase": 299.99
        },
        {
            "id": 2,
            "name": "Bob Williams",
            "email": "bob@email.com",
            "phone": "(555) 333-4444",
            "address": "789 Pine Street",
            "location": {"latitude": 41.8781, "longitude": -87.6298},  # Chicago
            "balance": 2200.00,
            "last_purchase": 149.99
        },
        {
            "id": 3,
            "name": "Carol Davis",
            "email": "carol@email.com",
            "phone": "(555) 555-6666",
            "address": "321 Elm Drive",
            "location": {"latitude": 29.7604, "longitude": -95.3698},  # Houston
            "balance": 875.50,
            "last_purchase": 499.99
        }
    ]
    
    print("Original dataset:")
    print(json.dumps(customers[0], indent=2))
    print()
    
    # Define which fields need anonymization
    field_types = {
        "name": "name",
        "email": "email",
        "phone": "phone",
        "address": "address",
        "location": "geolocation",
        "balance": "monetary",
        "last_purchase": "monetary"
    }
    
    # Anonymize the dataset
    anonymizer = DataAnonymizer(seed=42)
    anonymized_customers = anonymizer.anonymize_dataset(
        customers,
        field_types,
        noise_radius_km=5
    )
    
    print("Anonymized dataset:")
    print(json.dumps(anonymized_customers[0], indent=2))
    print()
    
    # Verify mathematical properties are preserved
    original_total_balance = sum(c["balance"] for c in customers)
    anon_total_balance = sum(c["balance"] for c in anonymized_customers)
    
    print(f"Original total balance: ${original_total_balance:.2f}")
    print(f"Anonymized total balance: ${anon_total_balance:.2f}")
    print(f"Transformation preserved the sum structure")
    print()


def example_consistency():
    """Demonstrate consistent anonymization."""
    print("=== Consistency Check ===\n")
    
    anonymizer = DataAnonymizer(seed=42)
    
    # Same name should always map to same anonymized name
    name = "John Doe"
    anon1 = anonymizer.anonymize_name(name)
    anon2 = anonymizer.anonymize_name(name)
    
    print(f"First anonymization: {name} → {anon1}")
    print(f"Second anonymization: {name} → {anon2}")
    print(f"Consistent: {anon1 == anon2}")
    print()


if __name__ == "__main__":
    example_basic_anonymization()
    example_monetary_preservation()
    example_dataset_anonymization()
    example_consistency()
