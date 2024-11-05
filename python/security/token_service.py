from CustomException import CustomException

FILE = "security/blacklist.txt"


def write_to_blacklist(uuid, token):
    updated = False
    new_entry = f"{uuid}:{token}\n"
    with open(FILE, "r") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            stored_uuid, _ = line.strip().split(":")
            if stored_uuid == uuid:
                lines[i] = new_entry
                updated = True
                break
    if not updated:
        lines.append(new_entry)

    with open(FILE, "w") as file:
        file.writelines(lines)


def read_blacklist():
    blacklist = []
    try:
        with open(FILE, "r") as file:
            for line in file:
                uuid, token = line.strip().split(":")
                blacklist.append((uuid, token))
    except FileNotFoundError:
        raise CustomException("Eroare interna: fisier secret negasit", 500)

    return blacklist

#
# blacklist_data = read_blacklist()
# for uuid, token in blacklist_data:
#     print(f"UUID: {uuid}, Token: {token}")
