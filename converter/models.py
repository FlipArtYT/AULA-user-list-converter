from dataclasses import dataclass

@dataclass
class IservUser:
    group: str # 10FA
    lastname: str # Mustermann
    firstname: str # Max
    account: str # max.mustermann

@dataclass 
class AulaUser:
    realname: str # Max Mustermann
    displayname: str # Max M.
    username: str # maxmustermann
    email: str # max.example.com
    about_me: str # Hi, ich bin Max