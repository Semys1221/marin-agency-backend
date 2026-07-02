import os
import json
from pathlib import Path


class TestConfig:
    def test_read_config_demo_returns_dict(self):
        from cli.config import read_config
        cfg = read_config("marin", demo=True)
        assert isinstance(cfg, dict)
        assert cfg["tenant_id"] == "marin"
        assert "niches" in cfg

    def test_read_config_demo_contains_niches(self):
        from cli.config import read_config
        cfg = read_config("marin", demo=True)
        assert len(cfg["niches"]) > 0
        assert cfg["niches"][0]["name"] == "grossiste_beaute"

    def test_validate_config_valid(self):
        from cli.config import validate_config
        cfg = {"niches": [{"name": "test", "keywords": ["kw1"]}]}
        errors = validate_config(cfg)
        assert errors == []

    def test_validate_config_missing_niches(self):
        from cli.config import validate_config
        errors = validate_config({})
        assert "niches array is required" in errors

    def test_validate_config_missing_name(self):
        from cli.config import validate_config
        cfg = {"niches": [{"keywords": ["kw1"]}]}
        errors = validate_config(cfg)
        assert any("name is required" in e for e in errors)

    def test_validate_config_missing_keywords(self):
        from cli.config import validate_config
        cfg = {"niches": [{"name": "test"}]}
        errors = validate_config(cfg)
        assert any("keywords is required" in e for e in errors)


class TestDb:
    def test_is_configured_returns_false_without_env(self):
        from cli.db import is_configured
        assert is_configured() is False

    def test_is_configured_returns_false_with_placeholder(self, monkeypatch):
        from cli.db import is_configured
        monkeypatch.setenv("SUPABASE_URL", "...")
        monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "...")
        assert is_configured() is False

    def test_is_configured_returns_true_with_real_values(self, monkeypatch):
        from cli.db import is_configured
        monkeypatch.setenv("SUPABASE_URL", "https://test.supabase.co")
        monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "real-key-123")
        assert is_configured() is True

    def test_tenant_id_default(self):
        from cli.db import tenant_id
        tid = tenant_id()
        assert isinstance(tid, str)
        assert len(tid) > 0


class TestCreate:
    def test_create_tenant_creates_config_file(self, tmp_path):
        from cli.create import create_tenant
        import cli.create as create_mod
        original = create_mod.USERS_DIR
        create_mod.USERS_DIR = tmp_path / "users"
        try:
            path = create_tenant("test-tenant", [{"name": "niche1", "keywords": ["kw1"]}], target=5000)
            assert path.exists()
            with open(path) as f:
                data = json.load(f)
            assert data["tenant_id"] == "test-tenant"
            assert data["target"] == 5000
            assert len(data["niches"]) == 1
        finally:
            create_mod.USERS_DIR = original

    def test_create_tenant_with_multiple_niches(self, tmp_path):
        from cli.create import create_tenant
        import cli.create as create_mod
        original = create_mod.USERS_DIR
        create_mod.USERS_DIR = tmp_path / "users"
        try:
            niches = [
                {"name": "plombier", "keywords": ["plombier paris", "plombier lyon"]},
                {"name": "electricien", "keywords": ["electricien paris"]},
            ]
            path = create_tenant("test-tenant", niches, target=3000)
            with open(path) as f:
                data = json.load(f)
            assert len(data["niches"]) == 2
        finally:
            create_mod.USERS_DIR = original


class TestAi:
    def test_ia_available_false_without_key(self):
        from cli.ai import _ia_available
        assert _ia_available() is False

    def test_ia_available_false_with_placeholder(self, monkeypatch):
        from cli.ai import _ia_available
        monkeypatch.setenv("HERMES_API_KEY", "...")
        assert _ia_available() is False

    def test_ia_available_true_with_key(self, monkeypatch):
        from cli.ai import _ia_available
        monkeypatch.setenv("HERMES_API_KEY", "sk-real-key")
        assert _ia_available() is True

    def test_call_ia_returns_none_without_key(self):
        from cli.ai import _call_ia
        result = _call_ia("test prompt")
        assert result is None

    def test_parse_json_list_valid(self):
        from cli.ai import _parse_json_list
        result = _parse_json_list('["a", "b", "c"]')
        assert result == ["a", "b", "c"]

    def test_parse_json_list_with_markdown_fence(self):
        from cli.ai import _parse_json_list
        result = _parse_json_list('```json\n["a", "b"]\n```')
        assert result == ["a", "b"]

    def test_parse_json_list_none(self):
        from cli.ai import _parse_json_list
        assert _parse_json_list(None) is None

    def test_parse_json_list_invalid(self):
        from cli.ai import _parse_json_list
        assert _parse_json_list("not json") is None

    def test_parse_json_valid(self):
        from cli.ai import _parse_json
        result = _parse_json('{"key": "value"}')
        assert result == {"key": "value"}

    def test_parse_json_with_markdown_fence(self):
        from cli.ai import _parse_json
        result = _parse_json('```\n{"key": "value"}\n```')
        assert result == {"key": "value"}

    def test_parse_json_none(self):
        from cli.ai import _parse_json
        assert _parse_json(None) is None

    def test_parse_json_invalid(self):
        from cli.ai import _parse_json
        assert _parse_json("not json") is None


class TestSetup:
    def test_save_tenant_creates_json(self, tmp_path):
        from cli.setup import save_tenant
        import cli.setup as setup_mod
        original = setup_mod.USERS_DIR
        setup_mod.USERS_DIR = tmp_path / "users"
        try:
            path = save_tenant("test-tenant", [{"name": "n1", "keywords": ["k1"]}])
            assert path.exists()
            with open(path) as f:
                data = json.load(f)
            assert data["tenant_id"] == "test-tenant"
        finally:
            setup_mod.USERS_DIR = original

    def test_save_sequences_creates_json(self, tmp_path):
        from cli.setup import save_sequences
        import cli.setup as setup_mod
        original = setup_mod.USERS_DIR
        setup_mod.USERS_DIR = tmp_path / "users"
        try:
            path = save_sequences("test-tenant", {"niche1": {"steps": []}})
            assert path.exists()
            with open(path) as f:
                data = json.load(f)
            assert "niche1" in data
        finally:
            setup_mod.USERS_DIR = original
