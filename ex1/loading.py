from importlib import import_module


def check_dependency() -> bool:
    try:
        metadata = import_module("importlib.metadata")
        no_missing = True
        packages = {}
        missing: list[str] = []
        dependencies = [("pandas", "Data manipulation"),
                        ("numpy", "Numerical computation"),
                        ("matplotlib", "Visualization"),
                        ("requests", "Network access")]
        for dep, dep_descript in dependencies:
            try:
                import_module(dep)
                version = metadata.version(dep)
                print(f"[OK] {dep} ({version}) - {dep_descript} ready")
                packages[dep] = version
            except ImportError:
                if dep == "requests":
                    print(f"[OPTIONAL] {dep} not found")
                    continue
                no_missing = False
                print(f"[MISSING] {dep} - {dep_descript} not found\n"
                      f"    -> Install with pip: pip install {dep}\n"
                      f"    -> Or with poetry: poetry add {dep}")
                missing = missing + [dep]
        if no_missing is False:
            missing_str = ", ".join(missing)
            print("\nInstall all dependencies with the pip command: "
                  "pip install -r requirements.txt\n"
                  "Or with the poetry command: "
                  "poetry install -> poetry run python loading.py\n"
                  f"\nERROR: Missing required dependencies: {missing_str}"
                  ". Aborting.\n")
            return False
        return True
    except Exception as e:
        print(f"Error on checking_deps(): {e}")
        return False


def installed_dependencies() -> dict[str, str]:
    try:
        metadata = import_module("importlib.metadata")
        packages = {}
        dependencies = ["pandas", "numpy", "matplotlib", "requests"]
        for dep in dependencies:
            try:
                import_module(dep)
                version = metadata.version(dep)
                packages[dep] = version
            except ImportError:
                continue
        return packages
    except Exception:
        return {}


def parse_requirements() -> dict[str, str]:
    dependencies = [("pandas", "Data manipulation"),
                    ("numpy", "Numerical computation"),
                    ("matplotlib", "Visualization")]
    try:
        requirements = {}
        operators = ["==", "~=", ">=", "<=", ">", "<"]
        with open("requirements.txt", "r") as requirement_file:
            for line in requirement_file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                for operator in operators:
                    if operator in line:
                        package, version = line.split(operator, 1)
                        package = package.strip()
                        if package in [dep[0] for dep in dependencies]:
                            requirements[package] = (
                                operator + version.strip()
                            )
                        break
        for package, description in dependencies:
            if package not in requirements:
                requirements[package] = "not included"
        return requirements
    except Exception as e:
        print(f"Parse_requirements failed: {e}")
        return {}


def parse_pyproject() -> dict[str, str]:
    dependencies = [("pandas", "Data manipulation"),
                    ("numpy", "Numerical computation"),
                    ("matplotlib", "Visualization")]
    try:
        poetry_dependencies = {}
        inside_dependencies = False
        with open("pyproject.toml", "r") as toml_file:
            for line in toml_file:
                line = line.strip()
                if line == "[tool.poetry.dependencies]":
                    inside_dependencies = True
                    continue
                if line.startswith("[") and inside_dependencies:
                    break
                if not inside_dependencies or not line or line.startswith("#"):
                    continue
                package, version = line.split("=", 1)
                package = package.strip()
                if package in [dep[0] for dep in dependencies]:
                    poetry_dependencies[package] = (
                        version.strip().strip('"')
                    )
        for package, description in dependencies:
            if package not in poetry_dependencies:
                poetry_dependencies[package] = "not included"
        return poetry_dependencies
    except Exception as e:
        print(f"Parse_pyproject failed: {e}")
        return {}


def version_compare() -> None:
    installed_packages: dict | None = installed_dependencies()

    if not installed_packages:
        print("No installed packages available for comparison.")
        return
    dependencies = ["numpy", "pandas", "matplotlib"]
    print("\nINSTALLED VERSIONS:")
    for package in dependencies:
        version = installed_packages.get(package, "not installed")
        print(f"{package.capitalize()} - {version}")
    print("\nSPECIFICATIONS FROM requirements.txt:")
    requirements = parse_requirements()
    if requirements:
        for package in dependencies:
            version = requirements.get(package, "not included")
            print(f"{package.capitalize()} - {version}")
    else:
        print("Unable to retrieve requirements.txt specifications.")

    print("\nSPECIFICATIONS FROM pyproject.toml:")
    poetry_specs = parse_pyproject()
    if poetry_specs:
        for package in dependencies:
            version = poetry_specs.get(package, "not included")
            print(f"{package.capitalize()} - {version}")
    else:
        print("Unable to retrieve pyproject.toml specifications.")


def matrix_visualizer(data_frame) -> None:
    try:
        import matplotlib  # type: ignore[import-not-found]

        file_name = "matrix_analysis.png"
        matplotlib.figure(figsize=(10, 5))
        matplotlib.plot(data_frame["time"], data_frame["signal"])
        matplotlib.title("Matrix Signal Analysis")
        matplotlib.xlabel("Time")
        matplotlib.ylabel("Signal")
        matplotlib.grid(True)
        matplotlib.savefig(file_name)
        matplotlib.close()
        print("Analysis complete!\n"
              f"Results saved to: {file_name}")
    except Exception as e:
        print(f"Error on generate_visualization(): {e}")


def load_matrix() -> None:
    try:
        import numpy
        import pandas  # type: ignore[import-untyped]
        signal = numpy.random.rand(1000)
        time = numpy.arange(1000)
        data_frame = pandas.DataFrame({"time": time, "signal": signal})
        print("\nAnalyzing Matrix data...\n"
              "Processing 1000 data points...\n"
              "Generating visualization...\n\n")
        matrix_visualizer(data_frame)
    except Exception as e:
        print(f"Error on load_matrix(): {e}")


def loading() -> None:
    print("\nLOADING STATUS: Loading programs...\n"
          "Checking dependencies:\n")
    if check_dependency():
        load_matrix()
    show_version: bool = False
    if show_version:
        version_compare()
    print()
    print()


def main() -> None:
    loading()


if __name__ == "__main__":
    main()
