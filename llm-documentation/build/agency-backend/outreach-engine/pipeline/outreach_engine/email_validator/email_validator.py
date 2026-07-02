import asyncio
import json
import sys
import re
import dns.resolver
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("email_validator")

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

ROLE_BASED_PREFIXES = {
    "info", "contact", "support", "sales", "admin", "hello", "help",
    "marketing", "billing", "team", "noreply", "no-reply", "dev",
    "webmaster", "postmaster", "abuse", "careers", "jobs",
}

DISPOSABLE_DOMAINS = {
    "mailinator.com", "guerrillamail.com", "10minutemail.com",
    "tempmail.com", "throwaway.email", "yopmail.com", "sharklasers.com",
    "maildrop.cc", "inboxbear.com", "temp-mail.org", "trashmail.com",
    "mailnesia.com", "gettndenveremail.com", "getairmail.com",
    "emailondeck.com", "tempinbox.com", "mailmetrash.com",
    "spamgourmet.com", "sogetthis.com", "mailcatch.com",
    "discard.email", "mintemail.com", "spambox.us",
}


class ValidationResult:
    def __init__(self, email: str):
        self.email = email
        self.valid_format = False
        self.has_mx = False
        self.is_disposable = False
        self.is_role_based = False
        self.is_catch_all = False
        self.smtp_status: str | None = None
        self.error: str | None = None

    @property
    def is_valid(self) -> bool:
        if not self.valid_format:
            return False
        if self.is_disposable:
            return False
        if self.has_mx is False:
            return False
        return True

    @property
    def risk_score(self) -> str:
        if not self.is_valid:
            return "high"
        if self.is_role_based:
            return "medium"
        if self.is_catch_all:
            return "medium"
        if self.smtp_status == "unknown":
            return "medium"
        return "low"

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "valid_format": self.valid_format,
            "has_mx": self.has_mx,
            "is_disposable": self.is_disposable,
            "is_role_based": self.is_role_based,
            "is_catch_all": self.is_catch_all,
            "smtp_status": self.smtp_status,
            "is_valid": self.is_valid,
            "risk_score": self.risk_score,
            "error": self.error,
        }


def check_format(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def check_role_based(local_part: str) -> bool:
    return local_part.lower() in ROLE_BASED_PREFIXES


def check_disposable(domain: str) -> bool:
    return domain.lower() in DISPOSABLE_DOMAINS


def check_mx(domain: str) -> bool:
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=5)
        return len(answers) > 0
    except Exception:
        return False


async def check_smtp(email: str, domain: str, timeout: float = 5.0) -> str | None:
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(domain, 25), timeout=timeout
        )
        writer.write(b"EHLO validator\r\n")
        await writer.drain()

        writer.write(b"MAIL FROM:<check@validator.local>\r\n")
        await writer.drain()

        writer.write(f"RCPT TO:<{email}>\r\n".encode())
        await writer.drain()

        writer.write(b"QUIT\r\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return "unknown"
    except asyncio.TimeoutError:
        return "unknown"
    except ConnectionRefusedError:
        return "unknown"
    except Exception:
        return "unknown"


def check_catch_all(domain: str) -> bool:
    test_email = f"nonexistent-{hash(domain) & 0xFFFFFFFF}@{domain}"
    loop = asyncio.new_event_loop()
    try:
        status = loop.run_until_complete(check_smtp(test_email, domain))
        return status is not None
    finally:
        loop.close()


async def validate_email(email: str, smtp_check: bool = False, catch_all_check: bool = False) -> ValidationResult:
    result = ValidationResult(email)

    if not check_format(email):
        result.error = "invalid_format"
        return result
    result.valid_format = True

    _, domain = email.split("@")
    domain = domain.lower()

    local_part = email.split("@")[0]

    result.is_role_based = check_role_based(local_part)
    result.is_disposable = check_disposable(domain)

    if not check_mx(domain):
        result.error = "no_mx_record"
        return result
    result.has_mx = True

    if catch_all_check:
        result.is_catch_all = check_catch_all(domain)

    if smtp_check:
        result.smtp_status = await check_smtp(email, domain)

    return result


def main():
    emails = [e.strip() for e in sys.stdin.read().splitlines() if e.strip()]
    if not emails:
        log.error("Usage: cat emails.txt | python email_validator.py [--smtp] [--catchall]")
        sys.exit(1)

    smtp = "--smtp" in sys.argv
    catchall = "--catchall" in sys.argv

    results = asyncio.run(_validate_all(emails, smtp, catchall))

    valid = [r for r in results if r.is_valid]
    invalid = [r for r in results if not r.is_valid]

    log.info(f"\nChecked: {len(results)}, Valid: {len(valid)}, Invalid: {len(invalid)}")
    log.info(f"Risk breakdown: low={sum(1 for r in valid if r.risk_score == 'low')} "
             f"medium={sum(1 for r in valid if r.risk_score == 'medium')} "
             f"high={sum(1 for r in invalid if r.risk_score == 'high')}")

    print(json.dumps({"results": [r.to_dict() for r in results]}, indent=2))

    with open("valid_emails.txt", "w") as f:
        for r in valid:
            f.write(f"{r.email}\n")

    with open("invalid_emails.txt", "w") as f:
        for r in invalid:
            f.write(f"{r.email} | {r.error or r.risk_score}\n")


async def _validate_all(emails, smtp, catchall):
    tasks = [validate_email(e, smtp_check=smtp, catch_all_check=catchall) for e in emails]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    main()
