import os
import sys
from pathlib import Path
from typing import Dict, List

import requests
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory

CURSOR_UP_ONE = "\x1b[1A"
ERASE_LINE = "\x1b[2K"


def main():
    repo_owner = "j0rd1smit"
    repo_name = "cookiecutter_file_templates"
    history_path = Path.home() / f".local/share/{repo_name}/history"
    history_path.parent.mkdir(exist_ok=True, parents=True)

    res = requests.get(
        f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/info.json"
    )
    res.raise_for_status()
    dirs = sorted(res.json()["dirs"])
    current_node = Node.from_path(dirs)
    current_path = []

    try:
        while True:
            completer = get_completer(dirs, current_node, current_path)
            display_options(current_node.options)

            inputs = prompt(
                "/".join(current_path) + "/ > ",
                history=FileHistory(str(history_path)),
                auto_suggest=AutoSuggestFromHistory(),
                completer=completer,
            ).strip()
            clear_display_options(current_node.options)

            for item in inputs.split("/"):
                if item in current_node.options:
                    current_path.append(inputs)
                    current_node = current_node[inputs]

            if current_node.is_leaf:
                break

        selected = "/".join(current_path)
        os.system(
            f"cookiecutter https://github.com/{repo_owner}/{repo_name} --directory='{selected}'"
        )
    except KeyboardInterrupt:
        print("Cancelled by the user.")
        sys.exit(0)


def get_completer(dirs, current_node, current_path):
    current_path = "/".join(current_path)
    dirs_options = []
    for path in dirs:
        if current_path in path:
            path = path.replace("/cookiecutter.json", "").replace(current_path, "")
            if path[0] == "/":
                path = path[1:]
            dirs_options.append(path)

    options = sorted(list(set(current_node.options).union(set(dirs_options))))
    return WordCompleter(options, ignore_case=True)


def display_options(options):
    print("Select one of the following options:")
    for item in options:
        print(f"- {item}")


def clear_display_options(options):
    for _ in range(len(options) + 2):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
    sys.stdout.flush()


class Node:
    def __init__(self):
        self.children: Dict[str, "Node"] = {}

    @staticmethod
    def from_path(paths: List[str]) -> "Node":
        root = Node()

        for path in paths:
            current = root
            for folder in path.split("/"):
                if folder == "cookiecutter.json":
                    continue
                current = current[folder]

        return root

    @property
    def options(self) -> List[str]:
        return list(self.children.keys())

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def __getitem__(self, key: str) -> "Node":
        if key not in self.children:
            self.children[key] = Node()

        return self.children[key]

    def display(self, depth: int = 0) -> None:
        if len(self.children) == 0:
            return

        for k, v in self.children.items():
            print(" " * depth, "-", k)
            v.display(depth=depth + 2)


if __name__ == "__main__":
    main()
