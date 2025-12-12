# tests/unit/test_password_hashing.py

import pytest
from passlib.context import CryptContext

# Create a standalone pwd_context for unit tests (no database dependency)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestPasswordHashing:
    """Unit tests for password hashing and verification functionality."""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string hash."""
        password = "TestPass123"
        hashed = pwd_context.hash(password)
        
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_different_each_time(self):
        """Test that hash_password produces different hashes each time (bcrypt adds salt)."""
        password = "TestPass123"
        hash1 = pwd_context.hash(password)
        hash2 = pwd_context.hash(password)
        
        # Bcrypt adds salt, so hashes should differ
        assert hash1 != hash2
        # But both should be strings
        assert isinstance(hash1, str)
        assert isinstance(hash2, str)

    def test_hash_password_hides_original_password(self):
        """Test that hashed password doesn't contain the original password."""
        password = "TestPass123"
        hashed = pwd_context.hash(password)
        
        # Original password should not be in the hash
        assert password not in hashed

    def test_verify_password_correct_password(self):
        """Test that verify_password returns True for correct password."""
        password = "TestPass123"
        hashed = pwd_context.hash(password)
        
        assert pwd_context.verify(password, hashed) is True

    def test_verify_password_incorrect_password(self):
        """Test that verify_password returns False for incorrect password."""
        password = "TestPass123"
        hashed = pwd_context.hash(password)
        
        assert pwd_context.verify("WrongPass123", hashed) is False
        assert pwd_context.verify("wrongpass123", hashed) is False
        assert pwd_context.verify("", hashed) is False

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive."""
        password = "TestPass123"
        hashed = pwd_context.hash(password)
        
        # Different case should not match
        assert pwd_context.verify("testpass123", hashed) is False
        assert pwd_context.verify("TESTPASS123", hashed) is False
        
        # Exact case should match
        assert pwd_context.verify(password, hashed) is True

    def test_verify_password_empty_string(self):
        """Test that verify_password returns False for empty string."""
        password = "TestPass123"
        hashed = pwd_context.hash(password)
        
        assert pwd_context.verify("", hashed) is False

    def test_verify_password_with_special_characters(self):
        """Test password hashing with special characters."""
        password = "P@ssw0rd!#$%"
        hashed = pwd_context.hash(password)
        
        assert pwd_context.verify(password, hashed) is True
        assert pwd_context.verify("P@ssw0rd!#$", hashed) is False

    def test_verify_password_with_unicode(self):
        """Test password hashing with unicode characters."""
        password = "Tëst®Pass123"
        hashed = pwd_context.hash(password)
        
        assert pwd_context.verify(password, hashed) is True
        assert pwd_context.verify("Test®Pass123", hashed) is False

    def test_hash_consistency_with_bcrypt(self):
        """Test that hash uses bcrypt (hash starts with $2)."""
        password = "TestPass123"
        hashed = pwd_context.hash(password)
        
        # Bcrypt hashes start with these prefixes
        assert hashed.startswith("$2")

    def test_multiple_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes."""
        password1 = "Password123"
        password2 = "DifferentPass456"
        
        hash1 = pwd_context.hash(password1)
        hash2 = pwd_context.hash(password2)
        
        # Different passwords should have different hashes
        assert pwd_context.verify(password1, hash1) is True
        assert pwd_context.verify(password2, hash2) is True
        assert pwd_context.verify(password1, hash2) is False
        assert pwd_context.verify(password2, hash1) is False
