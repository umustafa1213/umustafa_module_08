import sys
import os
try:
    from dotenv import load_dotenv  # type: ignore[import-not-found]
except ImportError:
    print("Missing modules: 'python-dotenv'")
    print("run:\n pip install -r requirements.txt")
    sys.exit(1)


override_enabled: bool = True
valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
config_fail: list[str] = []

print("\nORACLE STATUS: Reading the Matrix...")
try:
    if not load_dotenv(override=override_enabled):
        raise FileNotFoundError(".env file not found")
except Exception as e:
    print(f"[ERROR] Failed to load configuration: {e}")
    sys.exit(1)

MATRIX_MODE: str | None = os.getenv("MATRIX_MODE")
DATABASE_URL: str | None = os.getenv("DATABASE_URL")
API_KEY: str | None = os.getenv("API_KEY")
LOG_LEVEL: str | None = os.getenv("LOG_LEVEL")
ZION_ENDPOINT: str | None = os.getenv("ZION_ENDPOINT")

if MATRIX_MODE == "development" or MATRIX_MODE == "production":
    print("\nConfiguration Loaded:")
    print(f"Mode: {MATRIX_MODE}")
    if (DATABASE_URL
            and (DATABASE_URL.startswith(("sqlite://", "postgresql://")))):
        print("Database: Connected to local instance")
    elif DATABASE_URL:
        print("Database: [ERROR] Invalid DATABASE_URL")
        config_fail.append("DATABASE_URL")
    else:
        print("Database: [ERROR] Missing DATABASE_URL")
        config_fail.append("DATABASE_URL")
    if API_KEY:
        print("API Access: Authenticated")
    else:
        print("API Access: [ERROR] Missing API_KEY")
        config_fail.append("API_KEY")
    if LOG_LEVEL in valid_levels:
        print(f"Log Level: {LOG_LEVEL}")
    else:
        print("Log Level: [ERROR] Missing or invalid LOG_LEVEL")
        config_fail.append("LOG_LEVEL")
    if ZION_ENDPOINT and ZION_ENDPOINT.startswith(("http://", "https://")):
        print("Zion Network: Online")
    elif ZION_ENDPOINT:
        config_fail.append("ZION_ENDPOINT")
        print("Zion Network: [ERROR] Invalid ZION_ENDPOINT")
    else:
        print("Zion Network: [ERROR] Missing ZION_ENDPOINT")
        config_fail.append("ZION_ENDPOINT")
else:
    print(f"[ERROR] Invalid MATRIX_MODE: {MATRIX_MODE}")
    print("Expected values: 'development' or 'production'")
    sys.exit(1)


def hard_coded_checker() -> bool:
    with open(__file__, "r") as file:
        content = file.read()
    hardcoded: list[str] = []
    config_names = (
        "MATRIX_MODE",
        "DATABASE_URL",
        "API_KEY",
        "LOG_LEVEL",
        "ZION_ENDPOINT"
    )
    for line in content.splitlines():
        line = line.strip()
        if "=" not in line:
            continue
        left, value = line.split("=", 1)
        name = left.strip().split(":")[0].strip()
        if name in config_names and "os.getenv(" not in value:
            hardcoded.append(name)
    if hardcoded:
        print("[WARNING] Hardcoded configuration variables: "
              f"{', '.join(hardcoded)}")
        return False
    print("[OK] No hardcoded configuration variables detected")
    return True


def env_checker() -> bool:
    if os.path.isfile(".env") and len(config_fail) == 0:
        print("[OK] .env file is properly configured")
        return True
    else:
        print("[KO] .env file is not properly configured")
        return False


def ovverride_checker() -> None:
    mode = MATRIX_MODE
    assert mode is not None
    if override_enabled:
        print(f"[OK] {mode.capitalize()} overrides available")
    else:
        print(f"[KO] {mode.capitalize()} overrides not available")


def env_security_check() -> None:
    print("\nEnvironment security check:")
    hard_coded_checker()
    configured: bool = env_checker()
    ovverride_checker()
    if not configured:
        print(
              f"\nMissing configuration: {', '.join(config_fail)}"
              "\nComplete configuration setting in respective .env file"
              "\n\nExiting program..."
             )
        sys.exit(1)


env_security_check()

print("\nThe Oracle sees all configurations.")
if MATRIX_MODE == "development":
    print("Development environment: Detailed diagnostics enabled")
elif MATRIX_MODE == "production":
    print("Production environment: Minimal diagnostics enabled")
