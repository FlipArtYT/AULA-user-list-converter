import csv
from pathlib import Path
from models import IservUser, AulaUser
from services.user_converters import IservToAulaUserConverter, IservToAulaCSVconverter
import io

input_csv_path = Path("assets/iserv.csv")


def main():
    parser = IservToAulaCSVconverter()
    result_csv = parser.convert_iserv_to_aula_csv_from_file(input_csv_path, Path.cwd() / "test.csv")

if __name__ == "__main__":
    main()