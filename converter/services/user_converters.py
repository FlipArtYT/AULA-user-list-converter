import csv
from pathlib import Path
from models import IservUser, AulaUser
from services.exceptions import InputFileNotExists
from services.constants import EMAIL_DOMAIN
from dataclasses import fields
import io

class IservToAulaCSVconverter:
    """
    A class to convert iServ user list CSVs to AULA user list CSVs.
    """

    def __init__(self):
        self.converter = IservToAulaUserConverter()

    def convert_iserv_to_aula_csv_from_file(self, input_path: Path, output_path: Path) -> list[dict]:
        if not input_path.is_file():
            return InputFileNotExists(
                "iServ user list was not found in the requested path", 
                input_path)
        
        with open(input_path, "r") as f:
            raw_input_csv: str = self._replace_semicolons(f.read())
            cured_raw_input_csv = io.StringIO(raw_input_csv)

            # Load iServ users and convert them to AULA users
            parsed_input_csv = list(csv.DictReader(cured_raw_input_csv))
            iserv_user_list = self.converter._load_iserv_csv_entries(parsed_input_csv)
            converted_user_list: list[AulaUser] = self.converter.convert_iserv_to_aula_user_list(iserv_user_list)

            output_csv_table = self.structure_user_list_as_csv_table(converted_user_list)

        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(output_csv_table)

    def structure_user_list_as_csv_table(self, user_list: list[AulaUser]) -> list[list[str]]:
        header = [field.name for field in fields(AulaUser)]
        csv_table = [header]

        for user in user_list:
            user_row = []

            for col in header:
                user_row.append(getattr(user, col))

            csv_table.append(user_row)

        return csv_table
        

    def _replace_semicolons(self, input_str: str):
        return input_str.replace(";", ",")

class IservToAulaUserConverter:
    """
    A class to convert iServ users to AULA users.
    """

    UMLAUT_EQUIVALENTS = (
        ("ä", "ae"),
        ("ö", "oe"),
        ("ü", "ue"),
    )

    def convert_iserv_to_aula_user_list(self, user_list: list[IservUser]) -> list[AulaUser]:
        aula_user_list = []

        for user in user_list:
            aula_user = self.convert_iserv_to_aula_user(user)
            aula_user_list.append(aula_user)

        return aula_user_list

    def convert_iserv_to_aula_user(self, user: IservUser) -> AulaUser:
        full_name = f"{user.firstname} {user.lastname}"
        display_name = f"{user.firstname} {user.lastname[:1]}."
        user_name = (f"{self._replace_umlaute(user.firstname.lower())}{self._replace_umlaute(user.lastname.lower())}").replace(" ", "")
        email = user.account + EMAIL_DOMAIN
        about_me = f"Hallo, ich bin {user.firstname}."

        return AulaUser(
            realname=full_name,
            displayname=display_name,
            username=user_name,
            email=email,
            about_me=about_me
        )

    def _load_iserv_csv_entries(self, iserv_entries: list[dict]) -> list[IservUser]:
        converted_iserv_account_list = []

        for entry in iserv_entries:
            iserv_user = self._load_iserv_csv_entry(entry)
            converted_iserv_account_list.append(iserv_user)

        return converted_iserv_account_list

    def _load_iserv_csv_entry(self, entry: dict) -> IservUser:
        user = IservUser(
            group=entry.get("\ufeffGruppe", "No group"),
            lastname=entry.get("Nachname", "No last name"),
            firstname=entry.get("Vorname", "No first name"),
            account=entry.get("Account", "No account id")
        )

        return user

    def _replace_umlaute(self, input_str: str):
        output_str = input_str
        
        for umlaut, replacement in self.UMLAUT_EQUIVALENTS:
            output_str = output_str.replace(umlaut, replacement)
        
        return output_str