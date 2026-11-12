import sys
import os
try:
    from dotenv import load_dotenv
except ImportError:
    print("Missing modules: 'python-dotenv'")
    print("run:\n pip install -r requirements.txt")
    sys.exit(1)


override_enabled: bool = True
var_dict: dict[str, str | None] = {
            "MATRIX_MODE": "",
            "DATABASE_URL": "",
            "API_KEY": "",
            "LOG_LEVEL": "",
            "ZION_ENDPOINT": "",
           }
valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
config_fail: list[str] = []

print("\nORACLE STATUS: Reading the Matrix...")
try:
    if not load_dotenv(override=override_enabled):
        raise FileNotFoundError(".env file not found")
except Exception as e:
    print(f"[ERROR] Failed to load configuration: {e}")
    sys.exit(1)

DATABASE_URL = "sqlite://suspicious_database.db"

for name in var_dict.keys():
    var_dict[name] = os.getenv(name)
if (var_dict["MATRIX_MODE"] == "development" or
        var_dict["MATRIX_MODE"] == "production"):
    print("\nConfiguration Loaded:")
    print(f"Mode: {var_dict['MATRIX_MODE']}")
    if (
        var_dict["DATABASE_URL"] and
        var_dict["DATABASE_URL"].startswith(("sqlite://", "postgresql://"))
            ):
        print(f"Database_url: {var_dict["DATABASE_URL"]}")
        print("Database: Connected to local instance")
    elif (
        var_dict["DATABASE_URL"] and
        not var_dict["DATABASE_URL"].startswith(("sqlite://", "postgresql://"))
            ):
        print("Database: [ERROR] Invalid DATABASE_URL")
        config_fail.append("DATABASE_URL")
    else:
        print("Database: [ERROR] Missing DATABASE_URL")
        config_fail.append("DATABASE_URL")
    if var_dict["API_KEY"]:
        print("API Access: Authenticated")
    else:
        print("API Access: [ERROR] Missing API_KEY")
        config_fail.append("API_KEY")
    if var_dict["LOG_LEVEL"] in valid_levels:
        print(f"Log Level: {var_dict['LOG_LEVEL']}")
    else:
        print("Log Level: [ERROR] Missing LOG_LEVEL")
        config_fail.append("LOG_LEVEL")
    if (
        var_dict["ZION_ENDPOINT"] and
        var_dict["ZION_ENDPOINT"].startswith(("http://", "https://"))
            ):
        print("Zion Network: Online")
    elif (
        var_dict["ZION_ENDPOINT"] and
        not var_dict["ZION_ENDPOINT"].startswith(("http://", "https://"))
            ):
        config_fail.append("ZION_ENDPOINT")
        print("Zion Network: [ERROR] Invalid ZION_ENDPOINT")
    else:
        print("Zion Network: [ERROR] Missing ZION_ENDPOINT")
        config_fail.append("ZION_ENDPOINT")
else:
    print(f"[ERROR] Invalid MATRIX_MODE: {var_dict['MATRIX_MODE']}")
    print("Expected values: 'development' or 'production'")
    sys.exit(1)


def hard_coded_checker() -> bool:
    with open("oracle.py", "r") as file:
        content = file.read()
    hardcoded: list[str] = []
    for name in var_dict.keys():
        for line in content.splitlines():
            line = line.strip()
            if line.startswith(f"{name} ="):
                hardcoded.append(name)
                break
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
    mode: str | None = var_dict["MATRIX_MODE"]
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
