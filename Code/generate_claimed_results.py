import logging
import argparse
import pathlib
import os

from threading import active_count
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from random import shuffle
from tabulate import tabulate
from pathlib import Path
from functools import partial


from S_run_aifeynman import run_aifeynman

_CFG = {
  "dataset_path"      : "../Feynman_without_units/",
  "operations_file"   : "./14ops.txt",
  "polynomial_degree" : 3,
  "number_of_epochs"  : 500,
  "bruteforce_time"   : 60,
  "test_percentage"   : 0,
}

class RunAll:
    """
    Run the solver on the whole dataset
    """

    def __init__(self, *,  cfg=_CFG):
        logging.basicConfig(filename="output_no_units_parallel.log", level=logging.DEBUG)
        self.cfg = cfg
        self.results = {}

 
    def print_results(self):
        table = []
        for file, sol in self.results.items():
            table.append(sol[-1])
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
    
    def run_solver(self, dirs=None):
        if not dirs:
            path = Path(self.cfg["dataset_path"])
            dirs = list(path.iterdir())
            shuffle(dirs) # Shuffle to sample a different file each time
            
        else:
            path=Path(self.cfg["dataset_path"])
            child = dirs
            
            
#         for child in dirs:
#         print(child)
        print(f"Process PID: {os.getpid()} ---------------- Number of threads: {active_count()}" )
        self.results[str(child).split("/")[-1]] = run_aifeynman(
            pathdir=str(path.resolve()) + "/",
            filename=str(child).split("/")[-1],
            BF_try_time=int(self.cfg["bruteforce_time"]),
            BF_ops_file_type=Path(self.cfg["operations_file"]),
            polyfit_deg=int(self.cfg["polynomial_degree"]),
            NN_epochs=int(self.cfg["number_of_epochs"]),
            vars_name=[],
            test_percentage=int(self.cfg["test_percentage"]),
        )

        logging.info(self.results)
        print("@"*120)
        print("@"*120)

        self.print_results()


def get_files(dirs, chunks=5):
    dirs = list(path.iterdir())
    dirs = [file for file in dirs if not (str(file).endswith("test") or str(file).endswith("train"))]
    for i in range(0, len(dirs), chunks):
        yield dirs[i : i + chunks]

if __name__ == "__main__":

    #cfg_path = pathlib.Path("/home/aziz/lambda_lab/AI-Feynman/configs.cfg")
    #if cfg_path.exists():
    #    RunAll(cfg_path=cfg_path)
    #else:
    #    print(f"No such a file {cfg_path}")

    solver = RunAll().run_solver
    path = Path(_CFG["dataset_path"])
    #dirs = list(path.iterdir())
    #chunked_dirs = list(get_files(dirs, chunks=24))
# print(chunked_dirs[0], len(chunked_dirs[0]))
#    for dd in chunked_dirs:
 #       pool = Pool(len(dd))
  #      print(dd, len(dd))
    #    pool.map(print, dd)
   #     pool.map(solver, dd)
   # pool.close()
   
    parser = argparse.ArgumentParser(description='Solver')
    parser.add_argument('--file', help='Enter file path')

    args = parser.parse_args()
    solver(args.file)

