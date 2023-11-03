from pathlib import Path
import argparse
import os
import rmdup

def main():
    parser = argparse.ArgumentParser("rmdup", description="Prune duplicate files")
    parser.add_argument("path", type=Path)
    parser.add_argument("-n", "--dryrun", action="store_true", help="pretend to run, useful for testing.")
    parser.add_argument("-r", "--recursive", action="store_true", help="check directories within directories too?")
    args = parser.parse_args()

    # as a middle-man for os.remove()
    def do_remove_path(path: Path) -> None:
        print(f"-- Delete {str(path)}")
        if args.dryrun:
            return # stop here when it's a dryrun
        os.remove(str(path))

    def act_on_dir(dir_path: Path) -> None:
        for entry in rmdup.core.iter_entries(dir_path):
            for dup_path in entry.duplicates:
                do_remove_path(dup_path)
            print(f"++ Keep   {str(entry.main)}")

    if args.recursive:
        for dir_path in rmdup.core.find_directories(args.path):
            act_on_dir(dir_path)
    else:
        act_on_dir(args.path)

if __name__ == "__main__":
    main()
