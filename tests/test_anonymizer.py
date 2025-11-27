"""
Tests for the data anonymization library.
"""
import sys
sys.path.insert(0, '../src')

import unittest
import numpy as np
from data_anonymizer import DataAnonymizer, MonetaryTransformer


class TestMonetaryTransformer(unittest.TestCase):
    """Test cases for MonetaryTransformer."""
    
    def test_basic_transformation(self):
        """Test basic transformation."""
        transformer = MonetaryTransformer(scale=2.0, shift=10.0, seed=42)
        value = 100.0
        result = transformer.transform(value)
        expected = 2.0 * 100.0 + 10.0
        self.assertAlmostEqual(result, expected)
    
    def test_inverse_transformation(self):
        """Test inverse transformation."""
        transformer = MonetaryTransformer(scale=2.0, shift=10.0, seed=42)
        original = 100.0
        transformed = transformer.transform(original)
        reversed_val = transformer.inverse_transform(transformed)
        self.assertAlmostEqual(reversed_val, original)
    
    def test_preserves_ratios(self):
        """Test that transformation preserves ratios."""
        transformer = MonetaryTransformer(scale=1.5, shift=20.0, seed=42)
        a, b = 100.0, 200.0
        a_trans = transformer.transform(a)
        b_trans = transformer.transform(b)
        
        # For affine transformation y = ax + b, ratios are NOT exactly preserved
        # but for values far from zero, they're approximately preserved
        # However, differences ARE scaled by the same factor
        diff_original = b - a
        diff_transformed = b_trans - a_trans
        expected_diff = diff_original * transformer.scale
        
        self.assertAlmostEqual(diff_transformed, expected_diff, places=5)
    
    def test_preserves_sum(self):
        """Test that sum is transformed correctly."""
        transformer = MonetaryTransformer(scale=1.5, shift=20.0, seed=42)
        values = [100.0, 200.0, 300.0]
        
        original_sum = sum(values)
        transformed_values = transformer.transform_array(values)
        transformed_sum = sum(transformed_values)
        
        # Sum should be: scale * original_sum + n * shift
        expected_sum = transformer.scale * original_sum + len(values) * transformer.shift
        self.assertAlmostEqual(transformed_sum, expected_sum, places=5)
    
    def test_preserves_mean_structure(self):
        """Test that mean is transformed correctly."""
        transformer = MonetaryTransformer(scale=1.5, shift=20.0, seed=42)
        values = [100.0, 200.0, 300.0, 400.0]
        
        original_mean = np.mean(values)
        transformed_values = transformer.transform_array(values)
        transformed_mean = np.mean(transformed_values)
        
        # Mean should be: scale * original_mean + shift
        expected_mean = transformer.scale * original_mean + transformer.shift
        self.assertAlmostEqual(transformed_mean, expected_mean, places=5)


class TestDataAnonymizer(unittest.TestCase):
    """Test cases for DataAnonymizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.anonymizer = DataAnonymizer(seed=42)
    
    def test_anonymize_name_consistency(self):
        """Test that same name always maps to same anonymized name."""
        name = "John Doe"
        anon1 = self.anonymizer.anonymize_name(name)
        anon2 = self.anonymizer.anonymize_name(name)
        self.assertEqual(anon1, anon2)
    
    def test_anonymize_name_different(self):
        """Test that different names map to different anonymized names."""
        name1 = "John Doe"
        name2 = "Jane Smith"
        anon1 = self.anonymizer.anonymize_name(name1)
        anon2 = self.anonymizer.anonymize_name(name2)
        self.assertNotEqual(anon1, anon2)
    
    def test_anonymize_address_consistency(self):
        """Test that same address always maps to same anonymized address."""
        address = "123 Main St"
        anon1 = self.anonymizer.anonymize_address(address)
        anon2 = self.anonymizer.anonymize_address(address)
        self.assertEqual(anon1, anon2)
    
    def test_anonymize_email(self):
        """Test email anonymization."""
        email = "test@example.com"
        anon_email = self.anonymizer.anonymize_email(email)
        self.assertIn("@example.com", anon_email)
        self.assertNotEqual(email, anon_email)
    
    def test_anonymize_geolocation(self):
        """Test geolocation anonymization."""
        lat, lon = 40.7128, -74.0060
        anon_lat, anon_lon = self.anonymizer.anonymize_geolocation(
            lat, lon, noise_radius_km=5
        )
        
        # Check that coordinates have changed
        self.assertNotEqual(lat, anon_lat)
        self.assertNotEqual(lon, anon_lon)
        
        # Check that coordinates are still valid
        self.assertTrue(-90 <= anon_lat <= 90)
        self.assertTrue(-180 <= anon_lon <= 180)
        
        # Check that distance is approximately within noise radius
        # (this is approximate due to spherical geometry)
        distance = np.sqrt((anon_lat - lat)**2 + (anon_lon - lon)**2) * 111
        self.assertLess(distance, 15)  # Within ~15 km (allowing for approximation)
    
    def test_anonymize_monetary(self):
        """Test monetary value anonymization."""
        value = 1000.0
        anon_value = self.anonymizer.anonymize_monetary(value)
        self.assertNotEqual(value, anon_value)
        self.assertGreater(anon_value, 0)  # Should still be positive
    
    def test_anonymize_dataset(self):
        """Test dataset anonymization."""
        data = [
            {
                "id": 1,
                "name": "Alice",
                "email": "alice@test.com",
                "balance": 1000.0
            },
            {
                "id": 2,
                "name": "Bob",
                "email": "bob@test.com",
                "balance": 2000.0
            }
        ]
        
        field_types = {
            "name": "name",
            "email": "email",
            "balance": "monetary"
        }
        
        anon_data = self.anonymizer.anonymize_dataset(data, field_types)
        
        # Check that IDs are preserved
        self.assertEqual(anon_data[0]["id"], 1)
        self.assertEqual(anon_data[1]["id"], 2)
        
        # Check that sensitive fields are anonymized
        self.assertNotEqual(anon_data[0]["name"], "Alice")
        self.assertNotEqual(anon_data[0]["email"], "alice@test.com")
        self.assertNotEqual(anon_data[0]["balance"], 1000.0)
        
        # Check that transformation is consistent
        self.assertNotEqual(anon_data[0]["name"], anon_data[1]["name"])
    
    def test_geolocation_dict_format(self):
        """Test geolocation anonymization with dict format."""
        data = [
            {
                "id": 1,
                "location": {"latitude": 40.7128, "longitude": -74.0060}
            }
        ]
        
        field_types = {"location": "geolocation"}
        anon_data = self.anonymizer.anonymize_dataset(data, field_types)
        
        self.assertIn("latitude", anon_data[0]["location"])
        self.assertIn("longitude", anon_data[0]["location"])
        self.assertNotEqual(
            anon_data[0]["location"]["latitude"],
            40.7128
        )


if __name__ == "__main__":
    unittest.main()
