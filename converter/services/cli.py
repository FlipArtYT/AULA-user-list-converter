import argparse
from pathlib import Path
from services.user_converters import IservToAulaCSVconverter

def handle_args(args: argparse.Namespace):
    if args.input_path is not None:
        input_path = Path(args.input_path)
        output_path = Path(args.output_path) if args.output_path is not None else Path.cwd() / Path(input_path.stem + "_output.csv")

        try:
            parser = IservToAulaCSVconverter()
            parser.convert_iserv_to_aula_csv_from_file(input_path, output_path)

        except Exception as e:
            print(f"Failed to convert iServ user list CSV to AULA user list CSV: {e}")