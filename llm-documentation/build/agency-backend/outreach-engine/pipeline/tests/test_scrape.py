import json


class TestLeadFilter:
    def test_has_email_with_email(self):
        from outreach_engine.scrape.lead_filter import has_email
        assert has_email({"email": "a@b.com"}) is True

    def test_has_email_with_email_1(self):
        from outreach_engine.scrape.lead_filter import has_email
        assert has_email({"email_1": "a@b.com"}) is True

    def test_has_email_without_email(self):
        from outreach_engine.scrape.lead_filter import has_email
        assert has_email({"name": "test"}) is False

    def test_has_email_empty_string(self):
        from outreach_engine.scrape.lead_filter import has_email
        assert has_email({"email": ""}) is False

    def test_has_phone_with_phone(self):
        from outreach_engine.scrape.lead_filter import has_phone
        assert has_phone({"phone": "01 23"}) is True

    def test_has_phone_without_phone(self):
        from outreach_engine.scrape.lead_filter import has_phone
        assert has_phone({"name": "test"}) is False

    def test_has_phone_empty_string(self):
        from outreach_engine.scrape.lead_filter import has_phone
        assert has_phone({"phone": ""}) is False

    def test_is_valid_lead_with_email_only(self):
        from outreach_engine.scrape.lead_filter import is_valid_lead
        assert is_valid_lead({"email": "a@b.com"}) is True

    def test_is_valid_lead_with_phone_only(self):
        from outreach_engine.scrape.lead_filter import is_valid_lead
        assert is_valid_lead({"phone": "01 23"}) is True

    def test_is_valid_lead_with_both(self):
        from outreach_engine.scrape.lead_filter import is_valid_lead
        assert is_valid_lead({"email": "a@b.com", "phone": "01 23"}) is True

    def test_is_valid_lead_with_none(self):
        from outreach_engine.scrape.lead_filter import is_valid_lead
        assert is_valid_lead({"name": "test"}) is False

    def test_filter_leads(self, sample_leads):
        from outreach_engine.scrape.lead_filter import filter_leads
        result = filter_leads(sample_leads)
        assert len(result) == 3  # A, B, C are valid (D has nothing)

    def test_filter_leads_empty_list(self):
        from outreach_engine.scrape.lead_filter import filter_leads
        assert filter_leads([]) == []

    def test_filter_stats_counts(self, sample_leads):
        from outreach_engine.scrape.lead_filter import filter_stats
        stats = filter_stats(sample_leads)
        assert stats["total"] == 4
        assert stats["with_email"] == 2  # A and C
        assert stats["with_phone"] == 2  # A and B
        assert stats["valid"] == 3       # A, B, C
        assert stats["filtered_out"] == 1  # D


class TestExtractEmail:
    def test_extract_email_main_field(self):
        from outreach_engine.scrape.outscraper_scraper import extract_email
        assert extract_email({"email": "a@b.com"}) == "a@b.com"

    def test_extract_email_email_1(self):
        from outreach_engine.scrape.outscraper_scraper import extract_email
        assert extract_email({"email_1": "a@b.com"}) == "a@b.com"

    def test_extract_email_email_2(self):
        from outreach_engine.scrape.outscraper_scraper import extract_email
        assert extract_email({"email_2": "a@b.com"}) == "a@b.com"

    def test_extract_email_email_3(self):
        from outreach_engine.scrape.outscraper_scraper import extract_email
        assert extract_email({"email_3": "a@b.com"}) == "a@b.com"

    def test_extract_email_prefers_main(self):
        from outreach_engine.scrape.outscraper_scraper import extract_email
        assert extract_email({"email": "main@b.com", "email_1": "alt@b.com"}) == "main@b.com"

    def test_extract_email_none_when_missing(self):
        from outreach_engine.scrape.outscraper_scraper import extract_email
        assert extract_email({}) == ""

    def test_extract_email_none_when_empty(self):
        from outreach_engine.scrape.outscraper_scraper import extract_email
        assert extract_email({"email": ""}) == ""


class TestDomain:
    def test_domain_https(self):
        from outreach_engine.scrape.outscraper_scraper import _domain
        assert _domain("https://www.example.com") == "example.com"

    def test_domain_http(self):
        from outreach_engine.scrape.outscraper_scraper import _domain
        assert _domain("http://example.com") == "example.com"

    def test_domain_without_protocol(self):
        from outreach_engine.scrape.outscraper_scraper import _domain
        assert _domain("example.com") == "example.com"

    def test_domain_with_path(self):
        from outreach_engine.scrape.outscraper_scraper import _domain
        assert _domain("https://example.com/page") == "example.com"

    def test_domain_empty(self):
        from outreach_engine.scrape.outscraper_scraper import _domain
        assert _domain("") == ""


class TestToFlat:
    def test_to_flat_contains_key_fields(self):
        from outreach_engine.scrape.outscraper_scraper import to_flat
        entry = {
            "name": "Test",
            "email": "a@b.com",
            "phone": "01",
            "site": "https://example.com",
            "full_address": "Paris",
            "rating": 4.5,
            "reviews": 10,
            "latitude": 48.85,
            "longitude": 2.34,
            "category": "Plumber",
            "type": "Plumber",
            "reviews_distribution": {},
            "working_hours": {},
            "emails": ["a@b.com"],
            "phones": ["01"],
            "photo": "url",
            "timezone": "Europe/Paris",
            "street_address": "Rue X",
            "city": "Paris",
            "country": "France",
            "place_id": "xxx",
            "google_id": "yyy",
            "business_status": "OPERATIONAL",
            "about": "about text",
            "social_links": ["url"],
            "owner": "owner",
            "owner_link": "link",
        }
        flat = to_flat(entry)
        assert flat["name"] == "Test"
        assert flat["email"] == "a@b.com"
        assert flat["phone"] == "01"
        assert flat["site"] == "https://example.com"
        assert flat["full_address"] == "Paris"


class TestToCsvJson:
    def test_to_json_creates_valid_json(self, tmp_path, sample_leads):
        from outreach_engine.scrape.outscraper_scraper import to_json
        path = str(tmp_path / "test.json")
        to_json(sample_leads, path)
        with open(path) as f:
            data = json.load(f)
        assert len(data) == 4

    def test_to_csv_creates_file(self, tmp_path, sample_leads):
        from outreach_engine.scrape.outscraper_scraper import to_csv
        path = str(tmp_path / "test.csv")
        to_csv(sample_leads, path)
        assert tmp_path.joinpath("test.csv").exists()
        content = tmp_path.joinpath("test.csv").read_text()
        assert "email" in content
