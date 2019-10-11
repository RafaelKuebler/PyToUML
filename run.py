import os
import sys
import json
import logging
import datetime
from os import walk
from typing import List
from pathlib import Path

from desc import ClassDesc
from source_to_desc import analyze_py_file
from desc_to_uml import desc_to_uml


def main():
    configure_logger()

    all_classes: List[ClassDesc] = []

    if not os.path.exists("output"):
        os.makedirs("output")

    # in_path = input("Please provide the path to search in: ")
    in_path = Path(".")
    for dir_path, dir_names, file_names in walk(in_path):
        logging.info(f"Searching sources in {dir_path}")
        for file_name in file_names:
            if not file_name.endswith(".py"):
                continue
            file_path = Path(dir_path) / Path(file_name)
            logging.info(f"Analyzing file {file_path}...")
            classes = analyze_py_file(file_path)
            # export_json_file(classes, Path(f"./output/{file_name[:-3]}.json"))
            all_classes += classes

    desc_to_uml(all_classes, Path("./output/plantuml.txt"))
    os.startfile(Path("./output/plantuml.png"))


def configure_logger():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_filename = datetime.date.today()
    logging.basicConfig(filename=f'logs/{log_filename}.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def export_json_file(classes: List[ClassDesc], out_path: Path) -> None:
    logging.info(f"Exporting json to {out_path}")
    with out_path.open('w') as output:
        json.dump(classes, output, cls=MyEncoder, indent=2)


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


if __name__ == "__main__":
    main()
