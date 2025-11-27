"""
Example demonstrating Faker integration with locale support and new field types.
"""
import sys
sys.path.insert(0, '../src')

from data_anonymizer import DataAnonymizer
import json


def example_faker_names_addresses():
    """Show improved names and addresses with Faker."""
    print("=== Faker-Generated Names and Addresses ===\n")
    
    anonymizer = DataAnonymizer(seed=42, locale='en_US')
    
    # Multiple examples to show diversity
    names = [
        "John Smith",
        "Jane Doe", 
        "Robert Johnson",
        "Mary Williams",
        "James Brown"
    ]
    
    print("US English locale:")
    for name in names:
        anon = anonymizer.anonymize_name(name)
        print(f"  {name} → {anon}")
    
    print("\nAddresses:")
    addresses = [
        "123 Main St",
        "456 Oak Ave",
        "789 Pine Rd"
    ]
    
    for addr in addresses:
        anon = anonymizer.anonymize_address(addr)
        print(f"  {addr} → {anon}")
    
    print()


def example_locales():
    """Show different locale support."""
    print("=== Multi-Locale Support ===\n")
    
    original_name = "John Smith"
    original_address = "123 Main Street"
    
    locales = [
        ('en_US', 'US English'),
        ('es_ES', 'Spanish'),
        ('fr_FR', 'French'),
        ('de_DE', 'German'),
        ('ja_JP', 'Japanese')
    ]
    
    for locale_code, locale_name in locales:
        anonymizer = DataAnonymizer(seed=42, locale=locale_code)
        anon_name = anonymizer.anonymize_name(original_name)
        anon_address = anonymizer.anonymize_address(original_address)
        
        print(f"{locale_name} ({locale_code}):")
        print(f"  Name: {anon_name}")
        print(f"  Address: {anon_address}")
        print()


def example_new_field_types():
    """Demonstrate new field types: company, SSN, credit card."""
    print("=== New Field Types ===\n")
    
    anonymizer = DataAnonymizer(seed=42, locale='en_US')
    
    # Company names
    print("Company Names:")
    companies = ["Acme Corp", "TechCo Inc", "Global Industries"]
    for company in companies:
        anon = anonymizer.anonymize_company(company)
        print(f"  {company} → {anon}")
    
    # SSN
    print("\nSocial Security Numbers:")
    ssns = ["123-45-6789", "987-65-4321", "555-12-3456"]
    for ssn in ssns:
        anon = anonymizer.anonymize_ssn(ssn)
        print(f"  {ssn} → {anon}")
    
    # Credit Cards (Luhn-valid)
    print("\nCredit Card Numbers (Luhn-valid):")
    cards = ["4532-1234-5678-9010", "5425-2334-3010-9903", "3782-822463-10005"]
    for card in cards:
        anon = anonymizer.anonymize_credit_card(card)
        print(f"  {card} → {anon}")
    
    print()


def example_comprehensive_dataset():
    """Anonymize a comprehensive employee dataset with all new field types."""
    print("=== Comprehensive Employee Dataset ===\n")
    
    employees = [
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice@company.com",
            "phone": "(555) 123-4567",
            "company": "Tech Solutions Inc",
            "ssn": "123-45-6789",
            "credit_card": "4532-1234-5678-9010",
            "address": "123 Main Street",
            "salary": 75000.00,
            "location": {"latitude": 40.7128, "longitude": -74.0060}
        },
        {
            "id": 2,
            "name": "Bob Smith",
            "email": "bob@company.com",
            "phone": "(555) 987-6543",
            "company": "Data Corp",
            "ssn": "987-65-4321",
            "credit_card": "5425-2334-3010-9903",
            "address": "456 Oak Avenue",
            "salary": 82000.00,
            "location": {"latitude": 34.0522, "longitude": -118.2437}
        }
    ]
    
    print("Original Employee Record:")
    print(json.dumps(employees[0], indent=2))
    print()
    
    # Define field types
    field_types = {
        "name": "name",
        "email": "email",
        "phone": "phone",
        "company": "company",
        "ssn": "ssn",
        "credit_card": "credit_card",
        "address": "address",
        "salary": "monetary",
        "location": "geolocation"
    }
    
    # Anonymize with US locale
    anonymizer = DataAnonymizer(seed=42, locale='en_US')
    anonymized = anonymizer.anonymize_dataset(
        employees,
        field_types,
        noise_radius_km=5
    )
    
    print("Anonymized Employee Record:")
    print(json.dumps(anonymized[0], indent=2))
    print()
    
    # Verify consistency - same inputs produce same outputs
    print("Consistency Check:")
    anon1 = anonymizer.anonymize_name("Alice Johnson")
    anon2 = anonymizer.anonymize_name("Alice Johnson")
    print(f"  Alice Johnson → {anon1}")
    print(f"  Alice Johnson → {anon2}")
    print(f"  Consistent: {anon1 == anon2}")
    print()


def example_comparison_old_vs_new():
    """Compare diversity of old vs new approach."""
    print("=== Diversity Comparison ===\n")
    
    anonymizer = DataAnonymizer(seed=None, locale='en_US')
    
    print("Generating 20 random names with Faker:")
    names = [anonymizer.anonymize_name(f"Person{i}", consistent=False) for i in range(20)]
    unique_names = len(set(names))
    
    print(f"Sample names: {names[:10]}")
    print(f"Unique names out of 20: {unique_names}/20")
    print()
    
    print("This demonstrates much higher diversity than the previous")
    print("14 first names × 13 last names = 182 possible combinations.")
    print("Faker can generate millions of unique, realistic names!")
    print()


if __name__ == "__main__":
    example_faker_names_addresses()
    example_locales()
    example_new_field_types()
    example_comprehensive_dataset()
    example_comparison_old_vs_new()
