import importlib
import sys


def check_dependency() -> None:
    try:
        metadata = importlib.import_module("importlib.metadata")
        no_missing = True
        packages = {}
        missing: list[str] = []
        dependencies = [("pandas", "Data manipulation"),
                        ("numpy", "Numerical computation"),
                        ("requests", "Network access"),
                        ("matplotlib", "Visualization")]
        for dep, dep_descript in dependencies:
            try:
                package = importlib.import_module(dep)
                version = metadata.version(dep)
                print(f"[OK] {dep} ({version}) - {dep_descript} ready")
                packages[dep] = package
            except ImportError:
                if dep == "requests":
                    print(f"[OPTIONAL] {dep} not found")
                    pass
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
                  f"\nERROR: Missing required dependencies: {missing_str[:-2]}. "
                  "Aborting.\n")
            sys.exit(1)
        return
    except Exception as e:
        print(f"Error on checking_deps(): {e}")
        sys.exit(1)


def load_matrix() -> None:
    try:
        import numpy
        import pandas
        signal = numpy.random.rand(1000)
        time = numpy.arange(1000)
        data_frame = pandas.DataFrame({"time": time, "signal": signal})
        print("\nAnalyzing Matrix data...\n"
              "Processing 1000 data points...\n"
              "Generating visualization...\n\n")
        matrix_visualizer(data_frame)
    except Exception as e:
        print(f"Error on load_matrix(): {e}")


def matrix_visualizer(data_frame) -> None:
    try:
        plt = importlib.import_module("matplotlib.pyplot")

        file_name = "matrix_analysis.png"
        plt.figure(figsize=(10, 5))
        plt.plot(data_frame["time"], data_frame["signal"])
        plt.title("Matrix Signal Analysis")
        plt.xlabel("Time")
        plt.ylabel("Signal")
        plt.grid(True)
        plt.savefig(file_name)
        plt.close()
        print("Analysis complete!\n"
              f"Results saved to: {file_name}")
    except Exception as e:
        print(f"Error on generate_visualization(): {e}")


def loading() -> None:
    print("\nLOADING STATUS: Loading programs...\n"
          "Checking dependencies:\n")
    check_dependency()
    load_matrix()


def main() -> None:
    loading()


if __name__ == "__main__":
    main()
