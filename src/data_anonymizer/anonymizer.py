"""
Data anonymization module with preservation of mathematical properties.
"""
import hashlib
import random
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import numpy as np


class MonetaryTransformer:
    """
    Transforms monetary values while preserving mathematical properties.
    
    Uses affine transformation: y = ax + b
    Where operations like sum, mean, variance ratios are preserved.
    """
    
    def __init__(self, scale: float = None, shift: float = None, seed: int = None):
        """
        Initialize the monetary transformer.
        
        Args:
            scale: Multiplication factor (default: random between 0.8-1.2)
            shift: Addition factor (default: random between -100 and 100)
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        self.scale = scale if scale is not None else random.uniform(0.8, 1.2)
        self.shift = shift if shift is not None else random.uniform(-100, 100)
    
    def transform(self, value: float) -> float:
        """Apply affine transformation to a monetary value."""
        return self.scale * value + self.shift
    
    def transform_array(self, values: List[float]) -> List[float]:
        """Transform a list of monetary values."""
        return [self.transform(v) for v in values]
    
    def inverse_transform(self, value: float) -> float:
        """Reverse the transformation (for testing/validation)."""
        return (value - self.shift) / self.scale
    
    def get_params(self) -> Dict[str, float]:
        """Get transformation parameters."""
        return {"scale": self.scale, "shift": self.shift}


class DataAnonymizer:
    """Main anonymization class for various data types."""
    
    def __init__(self, seed: int = None):
        """
        Initialize the anonymizer.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        self.monetary_transformer = MonetaryTransformer(seed=seed)
        self._name_cache = {}
        self._address_cache = {}
        
    def anonymize_name(self, name: str, consistent: bool = True) -> str:
        """
        Anonymize a person's name.
        
        Args:
            name: Original name
            consistent: If True, same name always maps to same anonymized name
        
        Returns:
            Anonymized name
        """
        if consistent and name in self._name_cache:
            return self._name_cache[name]
        
        # Generate deterministic fake name based on hash
        if consistent:
            hash_val = int(hashlib.sha256(name.encode()).hexdigest(), 16)
            random.seed(hash_val)
        
        first_names = [
            "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn",
            "Avery", "Parker", "Reese", "Sage", "Rowan", "Blake", "Drew"
        ]
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
            "Davis", "Rodriguez", "Martinez", "Wilson", "Anderson", "Taylor"
        ]
        
        fake_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        if consistent:
            self._name_cache[name] = fake_name
            if self.seed is not None:
                random.seed(self.seed)
        
        return fake_name
    
    def anonymize_address(self, address: str, consistent: bool = True) -> str:
        """
        Anonymize a street address.
        
        Args:
            address: Original address
            consistent: If True, same address always maps to same anonymized address
        
        Returns:
            Anonymized address
        """
        if consistent and address in self._address_cache:
            return self._address_cache[address]
        
        if consistent:
            hash_val = int(hashlib.sha256(address.encode()).hexdigest(), 16)
            random.seed(hash_val)
        
        street_names = [
            "Oak", "Maple", "Cedar", "Pine", "Elm", "Birch", "Willow",
            "Main", "Park", "Lake", "River", "Hill", "Valley"
        ]
        street_types = ["St", "Ave", "Rd", "Ln", "Dr", "Ct", "Way", "Blvd"]
        
        number = random.randint(100, 9999)
        street = random.choice(street_names)
        st_type = random.choice(street_types)
        
        fake_address = f"{number} {street} {st_type}"
        
        if consistent:
            self._address_cache[address] = fake_address
            if self.seed is not None:
                random.seed(self.seed)
        
        return fake_address
    
    def anonymize_geolocation(
        self,
        latitude: float,
        longitude: float,
        noise_radius_km: float = 10.0
    ) -> tuple:
        """
        Anonymize GPS coordinates by adding controlled noise.
        
        Args:
            latitude: Original latitude
            longitude: Original longitude
            noise_radius_km: Maximum displacement in kilometers
        
        Returns:
            Tuple of (new_latitude, new_longitude)
        """
        # Convert km to approximate degrees (rough approximation)
        lat_noise = np.random.uniform(-noise_radius_km / 111.0, noise_radius_km / 111.0)
        lon_noise = np.random.uniform(
            -noise_radius_km / (111.0 * np.cos(np.radians(latitude))),
            noise_radius_km / (111.0 * np.cos(np.radians(latitude)))
        )
        
        new_lat = latitude + lat_noise
        new_lon = longitude + lon_noise
        
        # Clamp to valid ranges
        new_lat = max(-90, min(90, new_lat))
        new_lon = max(-180, min(180, new_lon))
        
        return new_lat, new_lon
    
    def anonymize_monetary(self, value: float) -> float:
        """
        Anonymize a monetary value while preserving mathematical properties.
        
        Args:
            value: Original monetary value
        
        Returns:
            Transformed monetary value
        """
        return self.monetary_transformer.transform(value)
    
    def anonymize_email(self, email: str, consistent: bool = True) -> str:
        """
        Anonymize an email address.
        
        Args:
            email: Original email
            consistent: If True, same email always maps to same anonymized email
        
        Returns:
            Anonymized email
        """
        if consistent:
            hash_val = hashlib.sha256(email.encode()).hexdigest()[:12]
            return f"user{hash_val}@example.com"
        else:
            random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=12))
            return f"user{random_str}@example.com"
    
    def anonymize_phone(self, phone: str, consistent: bool = True) -> str:
        """
        Anonymize a phone number.
        
        Args:
            phone: Original phone number
            consistent: If True, same phone always maps to same anonymized phone
        
        Returns:
            Anonymized phone number
        """
        if consistent:
            hash_val = int(hashlib.sha256(phone.encode()).hexdigest(), 16)
            random.seed(hash_val)
        
        # Generate US-style phone number
        area_code = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        
        fake_phone = f"({area_code}) {exchange}-{number}"
        
        if consistent and self.seed is not None:
            random.seed(self.seed)
        
        return fake_phone
    
    def anonymize_dataset(
        self,
        data: List[Dict[str, Any]],
        field_types: Dict[str, str],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Anonymize an entire dataset.
        
        Args:
            data: List of records (dictionaries)
            field_types: Mapping of field names to types
                        ('name', 'address', 'email', 'phone', 'monetary', 'geolocation')
            **kwargs: Additional parameters (e.g., noise_radius_km for geolocation)
        
        Returns:
            Anonymized dataset
        """
        anonymized_data = []
        
        for record in data:
            anonymized_record = record.copy()
            
            for field, field_type in field_types.items():
                if field not in record:
                    continue
                
                if field_type == 'name':
                    anonymized_record[field] = self.anonymize_name(record[field])
                elif field_type == 'address':
                    anonymized_record[field] = self.anonymize_address(record[field])
                elif field_type == 'email':
                    anonymized_record[field] = self.anonymize_email(record[field])
                elif field_type == 'phone':
                    anonymized_record[field] = self.anonymize_phone(record[field])
                elif field_type == 'monetary':
                    anonymized_record[field] = self.anonymize_monetary(record[field])
                elif field_type == 'geolocation':
                    # Expect tuple or dict with lat/lon
                    if isinstance(record[field], (tuple, list)):
                        lat, lon = record[field]
                        noise_radius = kwargs.get('noise_radius_km', 10.0)
                        anonymized_record[field] = self.anonymize_geolocation(
                            lat, lon, noise_radius
                        )
                    elif isinstance(record[field], dict):
                        lat = record[field].get('latitude') or record[field].get('lat')
                        lon = record[field].get('longitude') or record[field].get('lon')
                        noise_radius = kwargs.get('noise_radius_km', 10.0)
                        new_lat, new_lon = self.anonymize_geolocation(
                            lat, lon, noise_radius
                        )
                        anonymized_record[field] = {
                            'latitude': new_lat,
                            'longitude': new_lon
                        }
            
            anonymized_data.append(anonymized_record)
        
        return anonymized_data
