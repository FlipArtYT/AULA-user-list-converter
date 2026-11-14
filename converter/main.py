import argparse
from services.cli import handle_args

def main():
    parser = argparse.ArgumentParser(description="Convert iServ user list CSVs to AULA user list CSVs")
    parser.add_argument("-v", "--version", action="version", version="AULA-user-list-converter 0.1")
    parser.add_argument("-i", "--input-path", required=False, help="Path to the input the CSV file")
    parser.add_argument("-o", "--output-path", required=False, help="Path to the output the CSV file")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    handle_args(args)

if __name__ == "__main__":
    main()