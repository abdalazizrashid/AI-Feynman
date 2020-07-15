import logging
import pathlib
import configparser
from tabulate import tabulate
from pathlib import Path

from Code.S_run_aifeynman import run_aifeynman



class RunAll:
    """
    Run the solver on all the whole dataset
    """

    def __init__(self, *, cfg_path: Path):
        logging.basicConfig(filename="output.log", level=logging.DEBUG)
        self.config = configparser.ConfigParser()
        self.config.read(cfg_path)
        self.cfg = self.config["Default"]
        self.print_results()
        self.results = {}


        self.run_solver()

    def log_results(self):
        pass

    def print_results(self):
        table = [
            ["foo", 696000, 1989100000],
            ["bar", 6371, 5973.6],
            ["baz", 1737, 73.5],
            ["qux", 3390, 641.85],
        ]
        print(tabulate(
                table,
                headers=[
                    "Average error",
                    "Cumulative error",
                    "Error",
                    "Symbolic expression",
                ],
            )
        )

    def run_solver(self):
        path = Path(self.cfg["dataset_path"])
        for child in path.iterdir():
            self.results[str(child).split("/")[-1]] = run_aifeynman(
                pathdir="/home/aziz/lambda_lab/AI-Feynman/example_data/",#str(path.resolve()) + "/",
                filename="example2.txt",#str(child).split("/")[-1],
                BF_try_time=int(self.cfg["bruteforce_time"]),
                BF_ops_file_type=Path(self.cfg["operations_file"]),
                polyfit_deg=int(self.cfg["polynomial_degree"]),
                NN_epochs=int(self.cfg["number_of_epochs"]),
                vars_name=[],
                test_percentage=int(self.cfg["test_percentage"]),
            )
            logging.info(self.results)
            break

if __name__ == "__main__":
    cfg_path = pathlib.Path("/home/aziz/lambda_lab/AI-Feynman/configs.cfg")
    if cfg_path.exists():
        RunAll(cfg_path=cfg_path)
    else:
        print(f"No such a file {cfg_path}")
