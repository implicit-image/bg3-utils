#!/usr/bin/env python3
from progressions import Progressions
from pathlib import Path
from sys import argv

def main():
    path = Path("/home/b/Games/modding/bg3/progressions.lsx")
    # path = Path(argv[1])
    if not path.exists():
        print(f"File {path.resolve()} does not exist")
        exit()
    progs = Progressions(path)
    progs.test()


if __name__ == "__main__":
    main()
