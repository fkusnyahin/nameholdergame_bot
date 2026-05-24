import gspread
from oauth2client.service_account import ServiceAccountCredentials

CRED_FILE = "mob-bot-mobdatabase-ad563d57da55.json"

def get_mobs_from_sheets():
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            CRED_FILE,
            ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        client = gspread.authorize(creds)
        sheet = client.open("MobStats").sheet1
        rows = sheet.get_all_records()
        return rows
    except Exception as e:
        print(f"Ошибка: {e}")
        return []