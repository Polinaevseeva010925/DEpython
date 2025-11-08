from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re


# ЭТАП 1-2: Базовый класс Account с методами


class Account:  # Создаю базовый класс для моделирования банковского счёта

    _account_counter = 1000

    def __init__(self, account_holder, balance=0):  # Создание конструктора

        self._validate_holder_name(account_holder)  # Валидация имени владельца

        if balance < 0:  # Валидация начального баланса с исключением ошибки отрицательного
            raise ValueError("Начальный баланс не может быть отрицательным")

        self.holder = account_holder
        self._balance = balance

        Account._account_counter += 1  # Генерация номера счёта, начиная с 1000
        self.account_number = f"ACC-{Account._account_counter:04d}"

        self.operations_history = []  # История операций: список словарей

        if balance > 0:  # Если есть начальный баланс, добавляем запись о начислении
            self._add_operation('initial', balance, 'success')

    @staticmethod
    def _validate_holder_name(name):  # Создание метода для валидации имени владельца счёта.
        # Имя должно быть формата "Имя Фамилия", с заглавных букв, поддерживается кириллица и латиница
        pattern = r'^[А-Яа-яA-Za-z][а-яa-z]*\s[А-Яа-яA-Za-z][а-яa-z]*$'
        if not re.match(pattern, name):
            raise ValueError(
                f"Имя должно быть в формате 'Имя Фамилия' с заглавных букв, получено: {name}"
            )

    def _add_operation(self, operation_type, amount, status):  # Создание метода для добавления операции в историю счета

        operation = {  # Формат для хранения данных по операции
            'type': operation_type,
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self._balance,
            'status': status
        }
        self.operations_history.append(operation)  # Добавление новой записи с информацией об операции в формате словаря

    def deposit(self, amount):  # Создание метода для пополнения счета

        if amount <= 0:  # Если сумма пополнения будет отрицательной - делаем исключение ошибки
            raise ValueError("Сумма пополнения должна быть положительной")

        self._balance += amount  # Добавляем сумму пополнения к балансу
        self._add_operation('deposit', amount, 'success')  # Добавляем операцию в историю
        print(f"Пополнение на {amount}. Новый баланс: {self._balance}")

    def withdraw(self, amount):  # Создание метода для снятия со счета

        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")

        if self._balance >= amount:  # Проверка, что на счете достаточно средств и не уходим в минус
            self._balance -= amount  # Вычитание суммы снятия из баланса
            self._add_operation('withdraw', amount, 'success')  # Добавляем операцию в историю
            print(f"Снятие {amount}. Новый баланс: {self._balance}")
        else:
            self._add_operation('withdraw', amount, 'fail')
            print(f"Ошибка: недостаточно средств (требуется {amount}, баланс {self._balance})")

    def get_balance(self):  # Создание метода для отображения баланса
        return self._balance

    def get_history(self):  # Создание метода для возврата истории операций в виде списка словарей
        return self.operations_history

    def display_history(self):  # Создание метода для красивого вывода истории

        print(f"\n{'=' * 80}")
        print(f"История операций счёта {self.account_number} ({self.holder})")
        print(f"{'=' * 80}")

        if not self.operations_history:
            print("История операций пуста")
            return

        for i, op in enumerate(self.operations_history, 1):
            status_symbol = "✓" if op['status'] == 'success' else "✗"
            print(
                f"{i}. [{status_symbol}] {op['type']:10} | "
                f"Сумма: {op['amount']:>8.2f} | "
                f"Баланс: {op['balance_after']:>8.2f} | "
                f"Время: {op['timestamp'].strftime('%d.%m.%Y %H:%M:%S')}"
            )
        print(f"{'=' * 80}\n")

    def plot_history(self):  # Метод для создания датафрейма из истории операций

        if not self.operations_history:
            print("История операций пуста, визуализация невозможна")
            return None

        df = pd.DataFrame(self.operations_history)  # Создаём датафрейм из истории

        df['timestamp'] = pd.to_datetime(df['timestamp'])  # Преобразуем типы данных для удобства
        df = df.sort_values('timestamp')

        print("\nДатафрейм истории операций:")
        print(df)

        plt.figure(figsize=(10, 6))  # Построение линейного графика баланса во времени
        plt.plot(df['timestamp'], df['balance_after'], marker='o', color='blue')
        plt.title('История баланса счёта')
        plt.xlabel('Время операции')
        plt.ylabel('Баланс счёта (руб.)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        return df


# ЭТАП 4: Наследование и специализированные счета


class CheckingAccount(Account):  # Создаю класс Расчётный счёт (текущий счёт)

    account_type = "Checking"

    def __init__(self, account_holder, balance=0):  # Создание конструктора
        super().__init__(account_holder, balance)  # Вызываем конструктор базового класса с передачей тех же аргументов
        print(f"Создан расчётный счёт {self.account_number}")


class SavingsAccount(Account):  # Создаю класс Сберегательный счёт с процентами и ограничениями

    account_type = "Savings"

    def __init__(self, account_holder, balance=0):
        super().__init__(account_holder, balance)
        print(f"Создан сберегательный счёт {self.account_number}")

    def withdraw(self, amount):  # Создание метода для снятия денег со сбер. счета

        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")

        max_withdrawal = self._balance * 0.5  # Создание ограничения на снятие более чем 50% от баланса

        if amount > max_withdrawal:  # Проверка условия по списанию и добавление строки в историю
            self._add_operation('withdraw', amount, 'fail')
            print(
                f"Ошибка: со сберегательного счёта можно снять максимум 50% баланса "
                f"({max_withdrawal:.2f}), запрошено {amount}"
            )
        elif self._balance >= amount:
            self._balance -= amount
            self._add_operation('withdraw', amount, 'success')
            print(f"Снятие {amount}. Новый баланс: {self._balance}")
        else:
            self._add_operation('withdraw', amount, 'fail')
            print(f"Ошибка: недостаточно средств")

    def apply_interest(self, rate):  # Создание метода для начисления процентов на остаток счета

        if rate < 0:
            raise ValueError("Процентная ставка не может быть отрицательной")

        interest = self._balance * (rate / 100)  # Расчет суммы по процентам
        self._balance += interest
        self._add_operation('interest', interest, 'success')
        print(f"Начислены проценты: {interest:.2f}. Новый баланс: {self._balance}")

    def analyze_large_transactions(self, n=5):  # Создание метода для вывода 5 последних крупных операций

        if not self.operations_history:
            print("История операций пуста")
            return

        sorted_ops = sorted(  # Сортируем по сумме (на убывание), затем по дате
            self.operations_history,
            key=lambda x: (x['amount'], x['timestamp']),
            reverse=True
        )

        print(f"\nТоп {n} крупных операций:")  # Выводим результат сортировки (первые 5 позиций через цикл for)
        print(f"{'='*80}")

        for i, op in enumerate(sorted_ops[:n], 1):
            status_symbol = "✓" if op['status'] == 'success' else "✗"
            print(
                f"{i}. [{status_symbol}] {op['type']:10} | "
                f"Сумма: {op['amount']:>10.2f} | "
                f"Баланс: {op['balance_after']:>10.2f} | "
                f"Время: {op['timestamp'].strftime('%d.%m.%Y %H:%M:%S')}"
            )
        print(f"{'='*80}\n")


# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ


if __name__ == "__main__":

    print("="*80)
    print("ДЕМОНСТРАЦИЯ: БАЗОВЫЙ КЛАСС ACCOUNT")
    print("="*80 + "\n")

    account1 = Account("Полина Евсеева", 1000)  # Пример 1: Обычный счёт
    account1.deposit(500)
    account1.withdraw(300)
    account1.display_history()

    print("\n" + "="*80)
    print("ДЕМОНСТРАЦИЯ: РАСЧЁТНЫЙ И СБЕРЕГАТЕЛЬНЫЙ СЧЕТА")
    print("="*80 + "\n")

    checking = CheckingAccount("Александр Смирнов", 5000)  # Пример 2: Расчётный счёт
    checking.deposit(2000)
    checking.withdraw(1500)

    savings = SavingsAccount("Harry Potter", 10000)  # Пример 3: Сберегательный счёт
    savings.deposit(3000)
    savings.withdraw(6500)  # Пробуем снять 50% от 13000
    savings.apply_interest(7)
    savings.analyze_large_transactions(n=3)
    savings.display_history()
