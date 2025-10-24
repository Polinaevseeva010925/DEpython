import re

def remove_consecutive_duplicates(text):
    pattern = r'\b(\w+)( \1)+\b'
    return re.sub(pattern, r'\1', text, flags=re.IGNORECASE)

user_input = input("Введите текст: ")
result = remove_consecutive_duplicates(user_input)
print("Результат:", result)