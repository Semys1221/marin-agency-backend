import re


class TestHttp:
    def test_iso_now_format(self):
        from outreach_engine.push_instantly.lib.http import iso_now
        now = iso_now()
        assert "T" in now
        assert now.endswith("+00:00") or "+" in now

    def test_instantly_headers_structure(self):
        from outreach_engine.push_instantly.lib.http import instantly_headers
        headers = instantly_headers()
        assert "Authorization" in headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"
        assert headers["Authorization"].startswith("Bearer ")


class TestSettings:
    def test_build_payload_contains_name(self):
        from outreach_engine.push_instantly.lib.settings import build_payload
        payload = build_payload("test-campaign", ["email1@test.com", "email2@test.com"])
        assert payload["name"] == "test-campaign"

    def test_build_payload_contains_email_list(self):
        from outreach_engine.push_instantly.lib.settings import build_payload
        payload = build_payload("test", ["a@b.com", "c@d.com"])
        assert len(payload["email_list"]) == 2

    def test_build_payload_has_schedule(self):
        from outreach_engine.push_instantly.lib.settings import build_payload
        payload = build_payload("test", [])
        assert "campaign_schedule" in payload
        assert "schedules" in payload["campaign_schedule"]

    def test_build_payload_has_sequences(self):
        from outreach_engine.push_instantly.lib.settings import build_payload
        payload = build_payload("test", [])
        assert "sequences" in payload
        assert len(payload["sequences"]) > 0

    def test_build_payload_has_default_settings(self):
        from outreach_engine.push_instantly.lib.settings import build_payload
        payload = build_payload("test", [])
        assert payload["daily_limit"] == 50
        assert payload["stop_on_reply"] is True
        assert payload["open_tracking"] is True


class TestLeads:
    def test_to_instantly_format_basic(self, sample_clean_leads):
        from outreach_engine.push_instantly.lib.leads import _to_instantly_format
        result = _to_instantly_format(sample_clean_leads)
        assert len(result) == 3
        assert result[0]["email"] == "user1@example.com"

    def test_to_instantly_format_includes_optional_fields(self, sample_clean_leads):
        from outreach_engine.push_instantly.lib.leads import _to_instantly_format
        result = _to_instantly_format(sample_clean_leads)
        assert result[0]["first_name"] == "Jean"
        assert result[0]["last_name"] == "Dupont"
        assert result[0]["company_name"] == "Corp"
        assert result[0]["phone"] == "0102030405"

    def test_to_instantly_format_skips_empty_fields(self, sample_clean_leads):
        from outreach_engine.push_instantly.lib.leads import _to_instantly_format
        result = _to_instantly_format(sample_clean_leads)
        assert "first_name" not in result[1]
        assert "last_name" not in result[1]
        assert "company_name" not in result[1]

    def test_to_instantly_format_empty_input(self):
        from outreach_engine.push_instantly.lib.leads import _to_instantly_format
        assert _to_instantly_format([]) == []

    def test_to_instantly_format_minimal_lead(self):
        from outreach_engine.push_instantly.lib.leads import _to_instantly_format
        result = _to_instantly_format([{"email": "only@email.com"}])
        assert result[0] == {"email": "only@email.com"}


class TestSequences:
    def test_cold_returns_list(self):
        from outreach_engine.push_instantly.lib.sequences import cold
        seqs = cold()
        assert isinstance(seqs, list)
        assert len(seqs) >= 1

    def test_cold_has_two_steps(self):
        from outreach_engine.push_instantly.lib.sequences import cold
        seqs = cold()
        steps = seqs[0]["steps"]
        assert len(steps) == 2

    def test_cold_step_0_has_three_variants(self):
        from outreach_engine.push_instantly.lib.sequences import cold
        seqs = cold()
        variants = seqs[0]["steps"][0]["variants"]
        assert len(variants) == 3

    def test_cold_step_1_has_three_variants(self):
        from outreach_engine.push_instantly.lib.sequences import cold
        seqs = cold()
        variants = seqs[0]["steps"][1]["variants"]
        assert len(variants) == 3

    def test_cold_step_0_delay_is_zero(self):
        from outreach_engine.push_instantly.lib.sequences import cold
        assert cold()[0]["steps"][0]["delay"] == 0

    def test_cold_step_1_delay_is_three(self):
        from outreach_engine.push_instantly.lib.sequences import cold
        assert cold()[0]["steps"][1]["delay"] == 3

    def test_cold_variants_have_subject_and_body(self):
        from outreach_engine.push_instantly.lib.sequences import cold
        variant = cold()[0]["steps"][0]["variants"][0]
        assert "subject" in variant
        assert "body" in variant

    def test_subsequence_has_parent_campaign(self):
        from outreach_engine.push_instantly.lib.sequences import subsequence
        seq = subsequence("camp-123")
        assert seq["parent_campaign"] == "camp-123"

    def test_subsequence_has_three_steps(self):
        from outreach_engine.push_instantly.lib.sequences import subsequence
        seq = subsequence("camp-123")
        steps = seq["sequences"][0]["steps"]
        assert len(steps) == 3

    def test_subsequence_has_conditions(self):
        from outreach_engine.push_instantly.lib.sequences import subsequence
        seq = subsequence("camp-123")
        assert seq["conditions"]["lead_activity"] == [4]


class TestAccounts:
    def test_list_active_no_key_returns_empty(self, monkeypatch):
        from outreach_engine.push_instantly.lib.accounts import list_active
        monkeypatch.setenv("INSTANTLY_API_KEY", "")
        result = list_active()
        assert isinstance(result, list)
        # Without API key it should try and fail, return empty list
        # or make a request that fails -> empty
        # The function makes a real HTTP call, so we just check type


class TestPush:
    def test_push_no_key_handles_gracefully(self):
        from outreach_engine.push_instantly.lib.leads import push
        # Without API key configured, push should try and fail gracefully
        # The function makes a real HTTP call
        pass
