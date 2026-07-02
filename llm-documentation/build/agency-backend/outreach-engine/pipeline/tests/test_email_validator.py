import pytest


class TestCheckFormat:
    def test_valid_email(self):
        from outreach_engine.email_validator.email_validator import check_format
        assert check_format("user@example.com") is True

    def test_valid_email_with_plus(self):
        from outreach_engine.email_validator.email_validator import check_format
        assert check_format("user+tag@example.com") is True

    def test_valid_email_with_dots(self):
        from outreach_engine.email_validator.email_validator import check_format
        assert check_format("first.last@example.co.uk") is True

    def test_invalid_email_no_at(self):
        from outreach_engine.email_validator.email_validator import check_format
        assert check_format("userexample.com") is False

    def test_invalid_email_no_domain(self):
        from outreach_engine.email_validator.email_validator import check_format
        assert check_format("user@") is False

    def test_invalid_email_spaces(self):
        from outreach_engine.email_validator.email_validator import check_format
        assert check_format("user @example.com") is False

    def test_empty_string(self):
        from outreach_engine.email_validator.email_validator import check_format
        assert check_format("") is False


class TestCheckRoleBased:
    def test_info_is_role(self):
        from outreach_engine.email_validator.email_validator import check_role_based
        assert check_role_based("info") is True

    def test_contact_is_role(self):
        from outreach_engine.email_validator.email_validator import check_role_based
        assert check_role_based("contact") is True

    def test_support_is_role(self):
        from outreach_engine.email_validator.email_validator import check_role_based
        assert check_role_based("support") is True

    def test_jean_is_not_role(self):
        from outreach_engine.email_validator.email_validator import check_role_based
        assert check_role_based("jean") is False

    def test_empty_is_not_role(self):
        from outreach_engine.email_validator.email_validator import check_role_based
        assert check_role_based("") is False


class TestCheckDisposable:
    def test_yopmail_is_disposable(self):
        from outreach_engine.email_validator.email_validator import check_disposable
        assert check_disposable("yopmail.com") is True

    def test_guerrillamail_is_disposable(self):
        from outreach_engine.email_validator.email_validator import check_disposable
        assert check_disposable("guerrillamail.com") is True

    def test_mailinator_is_disposable(self):
        from outreach_engine.email_validator.email_validator import check_disposable
        assert check_disposable("mailinator.com") is True

    def test_gmail_is_not_disposable(self):
        from outreach_engine.email_validator.email_validator import check_disposable
        assert check_disposable("gmail.com") is False

    def test_empty_string(self):
        from outreach_engine.email_validator.email_validator import check_disposable
        assert check_disposable("") is False


class TestValidationResult:
    def test_is_valid_when_all_good(self):
        from outreach_engine.email_validator.email_validator import ValidationResult
        r = ValidationResult("test@example.com")
        r.valid_format = True
        r.has_mx = True
        r.is_disposable = False
        assert r.is_valid is True

    def test_is_valid_false_when_bad_format(self):
        from outreach_engine.email_validator.email_validator import ValidationResult
        r = ValidationResult("test@example.com")
        r.valid_format = False
        r.has_mx = True
        assert r.is_valid is False

    def test_is_valid_false_when_no_mx(self):
        from outreach_engine.email_validator.email_validator import ValidationResult
        r = ValidationResult("test@example.com")
        r.valid_format = True
        r.has_mx = False
        assert r.is_valid is False

    def test_is_valid_false_when_disposable(self):
        from outreach_engine.email_validator.email_validator import ValidationResult
        r = ValidationResult("test@example.com")
        r.valid_format = True
        r.has_mx = True
        r.is_disposable = True
        assert r.is_valid is False

    def test_risk_score_low_when_valid(self):
        from outreach_engine.email_validator.email_validator import ValidationResult
        r = ValidationResult("test@example.com")
        r.valid_format = True
        r.has_mx = True
        r.is_disposable = False
        r.is_role_based = False
        r.is_catch_all = False
        assert r.risk_score == "low"

    def test_risk_score_medium_when_catch_all(self):
        from outreach_engine.email_validator.email_validator import ValidationResult
        r = ValidationResult("test@example.com")
        r.valid_format = True
        r.has_mx = True
        r.is_disposable = False
        r.is_catch_all = True
        assert r.risk_score == "medium"

    def test_risk_score_medium_when_role_based(self):
        from outreach_engine.email_validator.email_validator import ValidationResult
        r = ValidationResult("test@example.com")
        r.valid_format = True
        r.has_mx = True
        r.is_role_based = True
        assert r.risk_score == "medium"

    def test_risk_score_high_when_invalid(self):
        from outreach_engine.email_validator.email_validator import ValidationResult
        r = ValidationResult("test@example.com")
        r.valid_format = False
        assert r.risk_score == "high"

    def test_to_dict_contains_all_fields(self):
        from outreach_engine.email_validator.email_validator import ValidationResult
        r = ValidationResult("test@example.com")
        d = r.to_dict()
        assert d["email"] == "test@example.com"
        assert "is_valid" in d
        assert "risk_score" in d
        assert "valid_format" in d
        assert "has_mx" in d
        assert "is_disposable" in d
        assert "is_role_based" in d
        assert "is_catch_all" in d


class TestCheckMx:
    def test_gmail_has_mx(self):
        from outreach_engine.email_validator.email_validator import check_mx
        assert check_mx("gmail.com") is True

    def test_yahoo_has_mx(self):
        from outreach_engine.email_validator.email_validator import check_mx
        assert check_mx("yahoo.com") is True

    def test_nonexistent_domain_no_mx(self):
        from outreach_engine.email_validator.email_validator import check_mx
        assert check_mx("thisdomaindefinitelydoesnotexist99999.com") is False

    def test_empty_domain(self):
        from outreach_engine.email_validator.email_validator import check_mx
        assert check_mx("") is False


class TestCleaner:
    @pytest.mark.asyncio
    async def test_clean_emails_demo_mode_returns_results(self):
        from outreach_engine.email_validator.cleaner import clean_emails
        results = await clean_emails(["test@example.com", "info@test.com"], demo=True)
        assert len(results) == 2
        assert results[0].email == "test@example.com"

    @pytest.mark.asyncio
    async def test_clean_emails_demo_mode_has_is_valid(self):
        from outreach_engine.email_validator.cleaner import clean_emails
        results = await clean_emails(["test@example.com"], demo=True)
        # Demo mode randomly sets validity, but should always have the field
        assert hasattr(results[0], "is_valid")

    @pytest.mark.asyncio
    async def test_clean_emails_demo_mode_different_emails(self):
        from outreach_engine.email_validator.cleaner import clean_emails
        results = await clean_emails(["a@b.com", "c@d.com", "e@f.com"], demo=True)
        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_clean_emails_empty_list(self):
        from outreach_engine.email_validator.cleaner import clean_emails
        results = await clean_emails([], demo=True)
        assert results == []


class TestMyEmailVerifier:
    def test_check_credits_returns_string(self):
        from outreach_engine.email_validator.myemailverifier_client import check_credits
        credits = check_credits()
        assert isinstance(credits, str)

    def test_verify_email_no_key_returns_unknown(self):
        from outreach_engine.email_validator.myemailverifier_client import verify_email
        result = verify_email("test@example.com", api_key="")
        assert result["Status"] == "Unknown"

    def test_verify_email_no_key_has_error(self):
        from outreach_engine.email_validator.myemailverifier_client import verify_email
        result = verify_email("test@example.com")
        assert "error" in result


class TestAsyncValidate:
    @pytest.mark.asyncio
    async def test_validate_email_validates_format(self):
        from outreach_engine.email_validator.email_validator import validate_email
        result = await validate_email("test@gmail.com")
        assert result.valid_format is True
        assert result.has_mx is True

    @pytest.mark.asyncio
    async def test_validate_email_invalid_format(self):
        from outreach_engine.email_validator.email_validator import validate_email
        result = await validate_email("not-an-email")
        assert result.valid_format is False

    @pytest.mark.asyncio
    async def test_validate_email_role_based_detected(self):
        from outreach_engine.email_validator.email_validator import validate_email
        result = await validate_email("info@gmail.com")
        assert result.is_role_based is True

    @pytest.mark.asyncio
    async def test_validate_email_disposable_detected(self):
        from outreach_engine.email_validator.email_validator import validate_email
        result = await validate_email("test@yopmail.com")
        assert result.is_disposable is True
