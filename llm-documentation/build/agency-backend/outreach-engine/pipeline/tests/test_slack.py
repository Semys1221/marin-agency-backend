class TestSlack:
    def test_is_configured_false_without_token(self):
        from slack_notifier.transport.client import _is_configured
        assert _is_configured() is False

    def test_is_configured_false_with_placeholder(self, monkeypatch):
        from slack_notifier.transport.client import _is_configured
        monkeypatch.setenv("SLACK_BOT_TOKEN", "...")
        assert _is_configured() is False

    def test_is_configured_true_with_token(self, monkeypatch):
        from slack_notifier.transport.client import _is_configured
        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-real-token")
        assert _is_configured() is True

    def test_send_message_no_config_does_not_crash(self):
        from slack_notifier.transport.client import send_message
        result = send_message("test")
        assert result is False

    def test_announce_niches_no_config_does_not_crash(self):
        from slack_notifier.data.notifier import announce_niches
        announce_niches("test-tenant", 5)

    def test_announce_error_no_config_does_not_crash(self):
        from slack_notifier.alerts.notifier import announce_error
        announce_error("test-tenant", "test error")

    def test_announce_decision_no_config_does_not_crash(self):
        from slack_notifier.campaign.notifier import announce_decision
        announce_decision("test-tenant", "niche1", "scrape", "test")
