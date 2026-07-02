class TestHoursSince:
    def test_hours_since_none(self):
        from rotation_engine.rotation_engine import _hours_since
        assert _hours_since(None) is None

    def test_hours_since_empty(self):
        from rotation_engine.rotation_engine import _hours_since
        assert _hours_since("") is None

    def test_hours_since_recent(self):
        from rotation_engine.rotation_engine import _hours_since
        from datetime import datetime, timezone
        recent = datetime.now(timezone.utc).isoformat()
        hours = _hours_since(recent)
        assert isinstance(hours, int)
        assert hours >= 0

    def test_hours_since_old(self):
        from rotation_engine.rotation_engine import _hours_since
        ts = "2024-01-01T00:00:00+00:00"
        hours = _hours_since(ts)
        assert hours is not None
        assert hours > 1000  # More than 1000 hours since Jan 2024


class TestDecide:
    def test_decide_demo_returns_list(self):
        from rotation_engine.rotation_engine import decide
        result = decide({"tenant_id": "marin"}, demo=True)
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_decide_demo_has_scrape_action(self):
        from rotation_engine.rotation_engine import decide
        result = decide({"tenant_id": "marin"}, demo=True)
        assert result[0]["action"] == "scrape"

    def test_decide_demo_has_niche(self):
        from rotation_engine.rotation_engine import decide
        result = decide({"tenant_id": "marin"}, demo=True)
        assert result[0]["niche"] == "grossiste_beaute"

    def test_decide_demo_has_reason(self):
        from rotation_engine.rotation_engine import decide
        result = decide({"tenant_id": "marin"}, demo=True)
        assert "reason" in result[0]

    def test_decide_empty_config_returns_wait(self, monkeypatch):
        from rotation_engine.rotation_engine import decide
        monkeypatch.setenv("SUPABASE_URL", "...")
        monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "...")
        result = decide({"tenant_id": "", "niches": []})
        assert len(result) >= 1
        assert result[0]["action"] == "wait"

    def test_decide_no_niches_returns_wait(self, monkeypatch):
        from rotation_engine.rotation_engine import decide
        monkeypatch.setenv("SUPABASE_URL", "...")
        monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "...")
        result = decide({"tenant_id": "marin", "niches": []})
        assert result[0]["action"] == "wait"


class TestDemoDecisions:
    def test_demo_decisions_structure(self):
        from rotation_engine.rotation_engine import _demo_decisions
        decisions = _demo_decisions()
        assert len(decisions) == 1
        d = decisions[0]
        assert d["action"] == "scrape"
        assert d["niche"] == "grossiste_beaute"
        assert d["reason"] == "Demo mode"
