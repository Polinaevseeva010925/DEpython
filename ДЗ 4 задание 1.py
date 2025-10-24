import re

def check_car_number(car_id):
    allowed_letters = 'АВЕКМНОРСТУХ'
    pattern = rf'^([{allowed_letters}])(\d{{3}})([{allowed_letters}]{{2}})(\d{{2,3}})$'

    match = re.match(pattern, car_id)
    if match:
        number_part = ''.join(match.groups()[:-1])
        region = match.group(4)
        return f"Номер {number_part} валиден. Регион: {region}."
    else:
        return "Номер не валиден."
car_number = input("Введите номер транспортного средства: ").upper()
result = check_car_number(car_number)
print(result)
