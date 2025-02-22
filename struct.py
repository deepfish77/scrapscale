import os


def print_directory_structure(startpath: str, indent_level: int = 0) -> None:
    """Recursively prints the directory structure starting from startpath."""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * (level + indent_level)
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (level + 1 + indent_level)
        for f in files:
            print(f"{subindent}{f}")


# print_directory_structure(".")
