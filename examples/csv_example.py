"""
Example showing how to anonymize data from CSV files.
"""
import sys
sys.path.insert(0, '../src')

import csv
import json
from data_anonymizer import DataAnonymizer


def create_sample_csv():
    """Create a sample CSV file with sensitive data."""
    data = [
        ["id", "name", "email", "phone", "address", "latitude", "longitude", "salary", "bonus"],
        ["1", "John Smith", "john.smith@company.com", "(555) 123-4567", "123 Main St", "40.7128", "-74.0060", "75000", "5000"],
        ["2", "Jane Doe", "jane.doe@company.com", "(555) 234-5678", "456 Oak Ave", "34.0522", "-118.2437", "82000", "6500"],
        ["3", "Bob Johnson", "bob.j@company.com", "(555) 345-6789", "789 Pine Rd", "41.8781", "-87.6298", "68000", "4200"],
    ]
    
    with open('sample_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print("Created sample_data.csv")


def anonymize_csv():
    """Read CSV, anonymize data, and write to new file."""
    # Read original data
    with open('sample_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        records = list(reader)
    
    print("\nOriginal data (first record):")
    print(json.dumps(records[0], indent=2))
    
    # Convert to appropriate types for processing
    for record in records:
        record['latitude'] = float(record['latitude'])
        record['longitude'] = float(record['longitude'])
        record['salary'] = float(record['salary'])
        record['bonus'] = float(record['bonus'])
    
    # Define field types for anonymization
    field_types = {
        'name': 'name',
        'email': 'email',
        'phone': 'phone',
        'address': 'address',
        'salary': 'monetary',
        'bonus': 'monetary'
    }
    
    # Create anonymizer with seed for reproducibility
    anonymizer = DataAnonymizer(seed=42)
    
    # Anonymize each record including geolocation
    anonymized_records = []
    for record in records:
        anon_record = record.copy()
        
        # Anonymize standard fields
        for field, field_type in field_types.items():
            if field_type == 'monetary':
                anon_record[field] = anonymizer.anonymize_monetary(record[field])
            elif field_type == 'name':
                anon_record[field] = anonymizer.anonymize_name(record[field])
            elif field_type == 'email':
                anon_record[field] = anonymizer.anonymize_email(record[field])
            elif field_type == 'phone':
                anon_record[field] = anonymizer.anonymize_phone(record[field])
            elif field_type == 'address':
                anon_record[field] = anonymizer.anonymize_address(record[field])
        
        # Anonymize geolocation separately
        new_lat, new_lon = anonymizer.anonymize_geolocation(
            record['latitude'],
            record['longitude'],
            noise_radius_km=5
        )
        anon_record['latitude'] = new_lat
        anon_record['longitude'] = new_lon
        
        anonymized_records.append(anon_record)
    
    print("\nAnonymized data (first record):")
    print(json.dumps(anonymized_records[0], indent=2))
    
    # Write anonymized data to new CSV
    fieldnames = records[0].keys()
    with open('anonymized_data.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(anonymized_records)
    
    print("\nCreated anonymized_data.csv")
    
    # Verify monetary properties preserved
    original_total_salary = sum(r['salary'] for r in records)
    anon_total_salary = sum(r['salary'] for r in anonymized_records)
    
    print(f"\nOriginal total salary: ${original_total_salary:,.2f}")
    print(f"Anonymized total salary: ${anon_total_salary:,.2f}")
    
    original_total_bonus = sum(r['bonus'] for r in records)
    anon_total_bonus = sum(r['bonus'] for r in anonymized_records)
    
    print(f"\nOriginal total bonus: ${original_total_bonus:,.2f}")
    print(f"Anonymized total bonus: ${anon_total_bonus:,.2f}")
    
    # Show that ratios between salary and bonus are approximately preserved
    print("\nSalary to Bonus ratios:")
    for i, (orig, anon) in enumerate(zip(records, anonymized_records)):
        orig_ratio = orig['salary'] / orig['bonus']
        anon_ratio = anon['salary'] / anon['bonus']
        print(f"  Record {i+1}: Original={orig_ratio:.2f}, Anonymized={anon_ratio:.2f}")


if __name__ == "__main__":
    create_sample_csv()
    anonymize_csv()
