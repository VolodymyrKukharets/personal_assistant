import pickle
import time
from collections import UserDict
from datetime import date, datetime
import re
import os


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        if self.validate_name(value):
            super().__init__(value)

    @staticmethod
    def validate_name(name):
        if len(name) >= 1:
            return name
        else:
            print("Ім'я не може бути пустим. Будь ласка, введіть ім'я.")
            return False

class Address(Field):
    def __init__(self, value):
        if self.validate_address(value):
            super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if self.validate_phone_number(value):
            super().__init__(value)

    @staticmethod
    def validate_phone_number(phone_num):
        if phone_num == 'вийти':
            return phone_num

        phone_num = re.sub(r'\D', '', phone_num)
        pattern = r"^(?:\+?380|0)\d{9}$"

        if re.match(pattern, phone_num):
            return phone_num
        else:
            print(f"Некоректний номер {phone_num}. Спробуйте ще раз. ")
            return False


class Email(Field):
    def __init__(self, value):
        if self.validate_email(value):
            super().__init__(value)

    @staticmethod
    def validate_email(email=None):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(pattern, email) or email is None or email == 'вийти':
            return email
        else:
            print(f"Некоректний email {email}. Спробуйте ще раз.")
            return False


class Birthday(Field):
    def __init__(self, value):
        if self.validate_data(value):
            super().__init__(value)

    @staticmethod
    def validate_data(birthday):
        if birthday == 'вийти':
            return birthday

        data_list = birthday.split("/")
        if len(data_list) == 3:
            day, month, year = map(int, data_list)
            current_year = datetime.now().year

            if 1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= current_year:
                return birthday
            else:
                print("Некоректний формат дати або рік занадто малий або перевищує поточний рік.")
                return False
        else:
            print("Некоректний формат дати. Використовуйте формат: 'dd/mm/yyyy'")
            return False


class Record:
    def __init__(self, name, address="", phone="", email="", birthday=""):
        self.name = name
        self.address = []
        self.phones = []
        self.emails = []
        self.birthday = birthday

        if address != "":
            self.address.append(address)
        if phone != "":
            self.phones.append(phone)
        if email != "":
            self.emails.append(email)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        else:
            today = date.today()
            # Перетворюємо рядок у дату за допомогою специфікації формату 'dd/mm/yyyy'
            birthday_date = datetime.strptime(self.birthday, '%d/%m/%Y').date()

            next_birthday = birthday_date.replace(year=today.year)

            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)

            days_to_birthday = (next_birthday - today).days
            return days_to_birthday


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.page_size = 3
        self.page_number = 0
    def add_record(self, record):
        self.data[record.name] = record

    def is_name_unique(self, name):
        for contact in self.data.values():
            if contact.name == name:
                print('Таке імя уже існує, введіть унікальне імя')
                return False
        return True

    def search_contacts(self, query):
        results = set()
        results.update([record for record in self.data.values() if query in record.name])
        results.update([record for record in self.data.values() if query in record.address])
        results.update([record for record in self.data.values() for phone in record.phones if query in phone])
        results.update([record for record in self.data.values() for email in record.emails if query in email])
        results.update([record for record in self.data.values() if query in record.birthday])
        return results

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)

    def __iter__(self):
        self.page_number = 0
        return self

    def __next__(self):
        items = list(self.data.values())
        items.sort(key=lambda contact: contact.name.lower())
        start_index = self.page_number * self.page_size
        end_index = start_index + self.page_size
        if start_index >= len(items):
            raise StopIteration()
        current_page_contacts = items[start_index:end_index]
        has_next_page = end_index < len(items)
        has_previous_page = self.page_number > 0
        return current_page_contacts, has_next_page, has_previous_page


address_book = AddressBook()

while True:
    print("1. Додати контакт")
    print("2. Зміна та видалення контактних данних")
    print("3. Пошук контакту")
    print("4. Вивід всіх контактів")
    print("5. Найближчі дні народження")
    print("6. Зберегти дані")
    print("7. Завантажити дані")
    print("8. Вийти")

    choice = input("Виберіть опцію: ")

    if choice == '1':
        os.system('cls')
        print("Додавання контакту:")
        print("Введіть 'вийти', щоб вийти з режиму додавання контакту.")
        name = Name.validate_name(input("Введіть ім'я: "))
        is_unique = address_book.is_name_unique(name)
        if name == 'вийти':
            print('Операція додавання контактів зупинена')
            time.sleep(2)
            os.system('cls')
            continue
        while name is False and is_unique is False:
            name = Name.validate_name(input("Введіть ім'я: "))
            if name == 'вийти':
                print('Операція додавання контактів зупинена')
                time.sleep(2)
                os.system('cls')
                break

        address = input("Введіть адресу: ")
        if name == 'вийти':
            print('Операція додавання контактів зупинена')
            time.sleep(2)
            os.system('cls')
            continue

        phone = Phone.validate_phone_number(input("Введіть номер телефону: "))
        if phone == 'вийти':
            print('Операція додавання контактів зупинена')
            time.sleep(2)
            os.system('cls')
            continue
        while phone is False:
            phone = Phone.validate_phone_number(input("Введіть номер телефону: "))
            if phone == 'вийти':
                print('Операція додавання контактів зупинена')
                time.sleep(2)
                os.system('cls')
                break

        email = Email.validate_email(input("Введіть email: "))
        if email == 'вийти':
            print('Операція додавання контактів зупинена')
            time.sleep(2)
            os.system('cls')
            continue
        while email is False:
            email = Email.validate_email(input("Введіть email: "))
            if email == 'вийти':
                print('Операція додавання контактів зупинена')
                time.sleep(2)
                os.system('cls')
                break

        birthday = Birthday.validate_data(input("Введіть дату народження в форматі dd/mm/yyyy: "))
        if birthday == 'вийти':
            print('Операція додавання контактів зупинена')
            continue
        while birthday is False:
            birthday = Birthday.validate_data(input("Введіть дату народження в форматі dd/mm/yyyy: "))
            if birthday == 'вийти':
                print('Операція додавання контактів зупинена')
                time.sleep(2)
                os.system('cls')
                break

        address_book.add_record(Record(name, address, phone, email, birthday))
        print('Запис створено')
        time.sleep(2)
        os.system('cls')

    elif choice == '2':
        os.system('cls')
        while True:
            print("1. Видалити контактні дані або контакт")
            print("2. Змінити дані контакту")
            print("3. Вихід")
            sub_choice = input("Виберіть опцію: ")

            if sub_choice == '1':
                os.system('cls')
                print("1. Видалити контакт")
                print("2. Видалити дані з контакту")
                print("3. Вихід")
                delete_choice = input("Виберіть опцію: ")

                if delete_choice == '1':
                    name_to_delete = input("Введіть ім'я контакту, який потрібно видалити: ")
                    records_to_delete = address_book.search_by_name(name_to_delete)
                    if records_to_delete:
                        for record in records_to_delete:
                            del address_book.data[record.name]
                        print(f"Контакти з іменем '{name_to_delete}' були видалені.")
                        time.sleep(2)
                        os.system('cls')
                    else:
                        print(f"Контакти з іменем '{name_to_delete}' не знайдені.")
                        time.sleep(2)
                        os.system('cls')

                elif delete_choice == '2':
                    os.system('cls')
                    print('1. Видалити адресу')
                    print('2. Видалити номер телефону')
                    print('3. Видалити email')
                    print('4. Видалити день народження')
                    print("5. Вихід")
                    delete_param_choice = input("Виберіть опцію: ")

                    if delete_param_choice == '1':
                        name_to_edit = input("Введіть імя контакту, з якого потрібно видалити адресу: ")
                        for name, record in address_book.data.items():
                            if name == name_to_edit:
                                print("Список адрес користувача:")
                                for i, address in enumerate(record.address, start=1):
                                    print(address)
                                address_to_delete = input("Введіть адресу для видалення: ")
                                if address_to_delete in record.address:
                                    record.address.remove(address_to_delete)
                                    print(f"Адреса {address_to_delete} видалена з контакту {name_to_edit}.")
                                    time.sleep(2)
                                    os.system('cls')
                                    break
                                else:
                                    print(f"Адреси '{address_to_delete}' не знайдено.")
                                    time.sleep(2)
                                    os.system('cls')
                            else:
                                print(f"Контакт з іменем '{name_to_edit}' не знайдений.")
                                time.sleep(2)
                                os.system('cls')

                    if delete_param_choice == '2':
                        name_to_edit = input("Введіть імя контакту, з якого потрібно видалити адресу: ")
                        for name, record in address_book.data.items():
                            if name == name_to_edit:
                                print("Список телефонів користувача:")
                                for i, phone in enumerate(record.phones, start=1):
                                    print(phone)
                                phone_to_delete = input("Введіть номер телефону для видалення: ")
                                if phone_to_delete in record.phones:
                                    record.phones.remove(phone_to_delete)
                                    print(f"Телефон {phone_to_delete} видалений з контакту {name_to_edit}.")
                                    time.sleep(2)
                                    os.system('cls')
                                    break
                                else:
                                    print(f"Телефон '{phone_to_delete}' не знайдено.")
                                    time.sleep(2)
                                    os.system('cls')
                            else:
                                print(f"Контакт з іменем '{name_to_edit}' не знайдений.")
                                time.sleep(2)
                                os.system('cls')


                    elif delete_param_choice == '3':
                        name_to_edit = input("Введіть імя контакту, з якого потрібно видалити адресу: ")
                        for name, record in address_book.data.items():
                            if name == name_to_edit:
                                print("Список емейлів користувача:")
                                for i, email in enumerate(record.emails, start=1):
                                    print(email)
                                email_to_delete = input("Введіть email для видалення: ")
                                if email_to_delete in record.emails:
                                    record.emails.remove(email_to_delete)
                                    print(f"Email {email_to_delete} видалений з контакту {name_to_edit}.")
                                    time.sleep(2)
                                    os.system('cls')
                                    break
                                else:
                                    print(f"Email '{email_to_delete}' не знайдено.")
                                    time.sleep(2)
                                    os.system('cls')
                            else:
                                print(f"Контакт з іменем '{name_to_edit}' не знайдений.")
                                time.sleep(2)
                                os.system('cls')


                    elif delete_param_choice == '4':
                        name_to_edit = input("Введіть ім'я контакту, з якого потрібно видалити день народження: ")
                        for name, record in address_book.data.items():
                            if name == name_to_edit:
                                record.birthday = ""
                                print(f"День народження видалено з контакту {name_to_edit}.")
                                time.sleep(2)
                                os.system('cls')
                                break
                        else:
                            print(f"Контакт з іменем '{name_to_edit}' не знайдений.")
                            time.sleep(2)
                            os.system('cls')

                    elif delete_param_choice == '5':
                        time.sleep(2)
                        os.system('cls')
                        break

                    else:
                        print('Некоректний ввід, повторіть спробу')


            elif sub_choice == '2':
                os.system('cls')
                contact_name = input("Введіть ім'я контакту, якого бажаєте змінити: ")
                if contact_name in address_book.data:
                    record = address_book.data[contact_name]

                    while True:
                        print("1. Змінити ім'я")
                        print("2. Змінити адресу")
                        print("3. Змінити номер телефону")
                        print("4. Змінити email")
                        print("5. Змінити дату народження")
                        print("6. Вихід")
                        change_choice = input("Виберіть опцію: ")

                        if change_choice == '1':
                            os.system('cls')
                            new_name = Name.validate_name(input("Введіть нове ім'я: "))

                            if new_name == 'вийти':
                                print('Зміна імені скасована')
                                time.sleep(2)
                                os.system('cls')
                                break

                            else:
                                del address_book.data[record.name]
                                record.name = new_name
                                address_book.add_record(record)
                                print("Ім'я змінене")
                                time.sleep(2)
                                os.system('cls')


                        elif change_choice == '2':
                            os.system('cls')
                            print("Виберіть адресу, яку хочете змінити:")
                            for i, address in enumerate(record.address, start=1):
                                print(f"{i}. {address}")
                            print(f"{len(record.address) + 1}. Додати нову адресу")
                            print(f"{len(record.address) + 2}. Вийти")
                            address_choice = input("Виберіть опцію: ")

                            if address_choice == str(len(record.address) + 1):
                                os.system('cls')
                                new_address = input("Введіть нову адресу: ")
                                if new_address == 'вийти':
                                    print('Додавання адреси скасовано')
                                    time.sleep(2)
                                    os.system('cls')
                                    break

                                else:
                                    record.address.append(new_address)
                                    print(f"Адреса '{new_address}' додана до контакту '{record.name}'.")
                                    time.sleep(2)
                                    os.system('cls')


                            elif address_choice == str(len(record.phones) + 2):
                                os.system('cls')
                                break

                            elif address_choice.isdigit() and 1 <= int(address_choice) <= len(record.address):
                                os.system('cls')
                                index_to_change = int(address_choice) - 1
                                old_address = record.address[index_to_change]
                                new_address = input(f"Введіть новий номер телефону для '{old_address}': ")
                                while new_address == False:
                                    new_phone = input(f"Введіть новий номер телефону для '{old_address}': ")

                                if new_address == 'вийти':
                                    print('Зміна номеру телефону скасована')
                                    time.sleep(2)
                                    os.system('cls')
                                    break

                                else:
                                    record.phones[index_to_change] = new_address
                                    print(
                                        f"Номер телефону '{old_address}' змінено на '{new_address}' для контакту '{record.name}'.")
                                    time.sleep(2)
                                    os.system('cls')

                            else:
                                print("Некоректний вибір, спробуйте ще раз.")
                                time.sleep(2)
                                os.system('cls')


                        elif change_choice == '3':
                            os.system('cls')
                            print("Виберіть номер телефону, який хочете змінити:")
                            for i, phone in enumerate(record.phones, start=1):
                                print(f"{i}. {phone}")
                            print(f"{len(record.phones) + 1}. Додати новий номер телефону")
                            print(f"{len(record.phones) + 2}. Вийти")
                            phone_choice = input("Виберіть опцію: ")

                            if phone_choice == str(len(record.phones) + 1):
                                os.system('cls')
                                new_phone = Phone.validate_phone_number(input("Введіть новий номер телефону: "))
                                if new_phone == 'вийти':
                                    print('Додавання номеру телефону скасовано')
                                    time.sleep(2)
                                    os.system('cls')
                                    break

                                else:
                                    record.phones.append(new_phone)
                                    print(f"Номер телефону '{new_phone}' додано до контакту '{record.name}'.")
                                    time.sleep(2)
                                    os.system('cls')


                            elif phone_choice == str(len(record.phones) + 2):
                                os.system('cls')
                                break

                            elif phone_choice.isdigit() and 1 <= int(phone_choice) <= len(record.phones):
                                os.system('cls')
                                index_to_change = int(phone_choice) - 1
                                old_phone = record.phones[index_to_change]
                                new_phone = Phone.validate_phone_number(
                                    input(f"Введіть новий номер телефону для '{old_phone}': "))
                                while new_phone == False:
                                    new_phone = Phone.validate_phone_number(
                                        input(f"Введіть новий номер телефону для '{old_phone}': "))

                                if new_phone == 'вийти':
                                    print('Зміна номеру телефону скасована')
                                    time.sleep(2)
                                    os.system('cls')
                                    break

                                else:
                                    record.phones[index_to_change] = new_phone
                                    print(
                                        f"Номер телефону '{old_phone}' змінено на '{new_phone}' для контакту '{record.name}'.")
                                    time.sleep(2)
                                    os.system('cls')

                            else:
                                print("Некоректний вибір, спробуйте ще раз.")
                                time.sleep(2)
                                os.system('cls')

                        elif change_choice == '4':
                            os.system('cls')
                            print("Виберіть email, який хочете змінити:")
                            for i, email in enumerate(record.emails, start=1):
                                print(f"{i}. {email}")
                            print(f"{len(record.emails) + 1}. Додати новий email")
                            print(f"{len(record.emails) + 2}. Вийти")
                            email_choice = input("Виберіть опцію: ")
                            if email_choice == str(len(record.emails) + 1):
                                os.system('cls')
                                new_email = Email.validate_email(input("Введіть новий email: "))
                                if new_email == 'вийти':
                                    print('Додавання email скасовано')
                                    time.sleep(2)
                                    os.system('cls')
                                    break

                                else:
                                    record.emails.append(new_email)
                                    print(f"Email '{new_email}' додано до контакту '{record.name}'.")
                                    time.sleep(2)
                                    os.system('cls')

                            elif email_choice == str(len(record.emails) + 2):
                                os.system('cls')
                                break


                            elif email_choice.isdigit() and 1 <= int(email_choice) <= len(record.emails):
                                os.system('cls')
                                index_to_change = int(email_choice) - 1
                                old_email = record.emails[index_to_change]
                                new_email = Email.validate_email(input(f"Введіть новий email для '{old_email}': "))
                                while new_email == False:
                                    new_email = Phone.validate_phone_number(
                                        input(f"Введіть новий email для '{old_email}': "))

                                if new_email == 'вийти':
                                    print('Зміна email скасована')
                                    time.sleep(2)
                                    os.system('cls')
                                    break

                                else:
                                    record.emails[index_to_change] = new_email
                                    print(f"Email '{old_email}' змінено на '{new_email}' для контакту '{record.name}'.")
                                    time.sleep(2)
                                    os.system('cls')

                            else:
                                print("Некоректний вибір, спробуйте ще раз.")
                                time.sleep(2)
                                os.system('cls')

                        elif change_choice == '5':
                            os.system('cls')
                            new_birthday = Birthday.validate_data(input("Введіть нову дату народження в форматі dd/mm/yyyy: "))
                            if new_birthday == 'вийти':
                                print('Зміна дати народження скасована')
                                time.sleep(2)
                                os.system('cls')
                                break

                            else:
                                record.birthday = new_birthday
                                print("Дата дня народження змінена")
                                time.sleep(2)
                                os.system('cls')

                        elif change_choice == '6':
                            os.system('cls')
                            break

                else:
                    print(f"Контакт з іменем '{contact_name}' не знайдений.")
                    time.sleep(2)
                    os.system('cls')


            elif sub_choice == '3':
                os.system('cls')
                break

            else:
                print('Некоректний ввід, повторіть спробу.')
                time.sleep(2)
                os.system('cls')

    elif choice == '3':
        os.system('cls')
        query = input("Введіть запит для пошуку: ")
        results = address_book.search_contacts(query)
        if results:
            for contact in results:
                address = ', '.join(contact.address)
                phones = ', '.join(contact.phones)
                emails = ', '.join(contact.emails)
                print(f"Ім'я: {contact.name}, Адреса: {address}, Телефон: {phones}, Email: {emails}, Birthday: {contact.birthday}")
            input('Введіть будь що для виходу')
            os.system('cls')
        else:
            print("Контакти не знайдені")
            time.sleep(2)
            os.system('cls')

    elif choice == '4':
        os.system('cls')
        while True:
            contacts, has_next_page, has_previous_page = next(address_book)
            if contacts:
                for contact in contacts:
                    if contact:
                        address = ', '.join(contact.address) if contact.address else "Немає адреси"
                        phones = ', '.join(contact.phones) if contact.phones else "Немає телефону"
                        emails = ', '.join(contact.emails) if contact.emails else "Немає email"
                        birthday = contact.birthday if contact.birthday else "Немає дати народження"
                        print(
                            f"Ім'я: {contact.name}, Адреса: {address}, Телефон: {phones}, Email: {emails}, Birthday: {birthday}")

                if has_next_page:
                    print(f"1. Наступна сторінка")

                if has_previous_page:
                    print(f"2. Попередня сторінка")

                print(f"3. Вихід")
                choice = input("Оберіть опцію: ")

                if choice.isdigit():
                    choice = int(choice)

                    if choice == 1 and has_next_page:
                        # Наступна сторінка
                        address_book.page_number += 1
                        os.system('cls')

                    elif choice == 2 and has_previous_page:
                        # Попередня сторінка
                        address_book.page_number -= 1
                        os.system('cls')

                    elif choice == 3:
                        # Вихід
                        os.system('cls')
                        break

                    else:
                        print("Некоректний ввід. Введіть опцію.")
                        time.sleep(2)
                        os.system('cls')

                else:
                    print("Некоректний ввід. Введіть опцію.")
                    time.sleep(2)
                    os.system('cls')

            else:
                print("Немає контактів.")
                input('Введіть будь що для виходу')
                os.system('cls')
                break



    elif choice == '5':
        os.system('cls')
        birthday_choice = input('Скільки днів до дня народження враховувати? ')
        closest_birthday_contacts = []
        for contact in address_book.data.values():
            days_to_birthday = contact.days_to_birthday()
            if days_to_birthday is not None and 0 <= days_to_birthday <= int(birthday_choice):
                closest_birthday_contacts.append(contact)
        if closest_birthday_contacts:
            closest_birthday_contacts.sort(key=lambda x: x.days_to_birthday())
            print("Найближчі дні народження:")
            for contact in closest_birthday_contacts:
                address = ', '.join(contact.address)
                phones = ', '.join(contact.phones)
                emails = ', '.join(contact.emails)
                print(
                    f"Ім'я: {contact.name}, Адреса: {address}, Телефон: {phones}, Email: {emails}, Birthday: {contact.birthday}")

        else:
            print("Немає контактів з найближчими днями народження.")
            time.sleep(2)
            os.system('cls')


    elif choice == '6':
        os.system('cls')
        filename = input("Введіть назву файлу для збереження: ")
        address_book.save_to_file(filename)
        print("Дані збережено")
        time.sleep(2)
        os.system('cls')

    elif choice == '7':
        os.system('cls')
        filename = input("Введіть назву файлу для завантаження: ")
        try:
            address_book.load_from_file(filename)
            print("Дані завантажено")
            time.sleep(2)
            os.system('cls')
        except:
            print("Файл не знайдено")
            time.sleep(2)
            os.system('cls')

    elif choice == '8':
        break

    else:
        print("Некоректний вибір, спробуйте ще раз.")
