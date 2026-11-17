import sys
import os
import site


def in_virtual_env() -> None:
    message: str = ""
    cur_path = sys.prefix
    base_path = sys.base_prefix
    if cur_path == base_path:
        print()
        print("Matix Status: You're still plugged in")
        print()
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print()
        message = (
            "WARNING: You're in the global environment!"
            "\nThe machines can see everything you install.\n\nTo enter the"
            " construct, run:\npython3 -m venv matrix_env\n"
            "source matrix_env/bin/activate # On Unix\n"
            "matrix_env\\Scripts\\activate # On Windows\n\n"
            "Then run this program again."
        )
        print(message)
    else:
        print()
        print("Matrix Status: Welcome to the construct")
        print()
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
        print(f"Environment Path: {sys.prefix}")
        print()
        message = (
            "SUCCESS: You're in an isolated environment!\n"
            "Safe to install packages without affecting\nthe global system.\n"
            "Package installation path:"
        )
        print(message)
        site_packages = site.getsitepackages()
        print(site_packages[0])


def main() -> None:
    in_virtual_env()


if __name__ == "__main__":
    main()
