import sys
import os
from pathlib import Path

# Ensure pipeline/ is on sys.path so all imports work
_pipeline_root = Path(__file__).resolve().parent.parent
if str(_pipeline_root) not in sys.path:
    sys.path.insert(0, str(_pipeline_root))

import pytest


@pytest.fixture
def sample_lead():
    return {
        "name": "Test SARL",
        "email": "contact@test.fr",
        "phone": "01 23 45 67 89",
        "site": "https://test.fr",
        "full_address": "Paris, France",
    }


@pytest.fixture
def sample_leads():
    return [
        {"name": "A", "email": "a@test.fr", "phone": "01"},
        {"name": "B", "email": "", "phone": "02"},
        {"name": "C", "email": "c@test.fr", "phone": ""},
        {"name": "D", "email": "", "phone": ""},
    ]


@pytest.fixture
def sample_clean_leads():
    return [
        {"email": "user1@example.com", "first_name": "Jean", "last_name": "Dupont", "company_name": "Corp", "phone": "0102030405"},
        {"email": "user2@example.com", "first_name": "", "last_name": "", "company_name": "", "phone": ""},
        {"email": "user3@example.com", "first_name": "Marie", "last_name": "Curie", "company_name": "Lab", "phone": ""},
    ]


