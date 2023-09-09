import pickle
from collections import UserDict
from datetime import datetime, date
import re


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        if self.validate_name(value):
            super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.validate_name(new_value):
            self._value = new_value

    @staticmethod
    def validate_name(name):
        if len(name) >= 1:
            return name
        else:
            print(f"Імя не може бути пустим. Будьласка, введіть імя.")
            return False

class Phone(Field):
    def __init__(self, value):
        if self.validate_phone_number(value):
            super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.validate_phone_number(new_value):
            self._value = new_value

    @staticmethod
    def validate_phone_number(phone_num):
        phone_num = re.sub(r'\D', '', phone_num)
        pattern = r"^(?:\+?380|0)\d{9}$"

        if re.match(pattern, phone_num) or phone_num == 'вийти':
            return phone_num
        else:
            print(f"Некорректний номер {phone_num}. Спробуйте ще раз. ")
            return False

class Email(Field):
    def __init__(self, value):
        if self.validate_email(value):
            super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.validate_email(new_value):
            self._value = new_value

    @staticmethod
    def validate_email(email=None):
        # Регулярний вираз для перевірки правильності формату електронної пошти
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Перевірка чи відповідає введений email заданому формату
        if re.match(pattern, email) or email == None or email == 'вийти':
            return email
        else:
            print(f"Некоректний email {email}. Спробуйте ще раз.")
            return False


class Birthday(Field):
    def __init__(self, value):
        if self.validate_data(value):
            super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.validate_data(new_value):
            self._value = new_value


    @staticmethod
    def validate_data(birthday):
        if birthday == 'вийти':
            return birthday

        # Validate the format of a birthday date
        data_list = birthday.split("/")
        if len(data_list) == 3:
            day, month, year = map(int, data_list)
            if (1 <= day <= 31 and 1 <= month <= 12):
                return birthday
        else:
            print("Некорректний формат дати. Використовуйте формат: 'dd/mm/yyyy'")
            return False


class Record:
    def __init__(self, name, phone="", email="", birthday=""):
        self.name = name
        self.phones = []
        self.emails = []
        self.birthday = birthday

        if phone != "":
            self.phones.append(phone)
        if email != "":
            self.emails.append(email)


    def add_phone(self, number):
        phone = Phone(number).value
        self.phones.append(phone)

    def remove_phone(self, number):
        index = self.find_phone_index(number)
        if index is not None:
            self.phones.pop(index)

    def edit_phone(self, old_number, new_number):
        index = self.find_phone_index(old_number)
        if index is not None:
            self.phones[index] = Phone(new_number).value

    def find_phone_index(self, number):
        for index, phone in enumerate(self.phones):
            if phone == number:
                return index
        return None

    def days_to_birthday(self):
        if not self.birthday:
            return None
        else:
            today = date.today()
            next_birthday = self.birthday.value.replace(year=today.year)

            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)

            days_to_birthday = (next_birthday - today).days
            return days_to_birthday


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name] = record

    def search_by_name(self, name):
        results = [record for record in self.data.values() if record.name == name]
        return results

    def search_by_phone(self, number):
        results = [record for record in self.data.values() for phone in record.phones if phone == number]
        return results
    def search_by_email(self, user_email):
        results = [record for record in self.data.values() for email in record.emails if email == user_email]
        return results
    def search_by_birthday(self, birthday):
        results = [record for record in self.data.values() if record.birthday == birthday]
        return results

    def search_contacts(self, query):
        results = []
        results.extend(self.search_by_name(query))
        results.extend(self.search_by_phone(query))
        results.extend(self.search_by_email(query))
        results.extend(self.search_by_birthday(query))
        return results

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)


address_book = AddressBook()

while True:
    print("1. Додати контакт")
    print("2. Змінити дані")
    print("3. Пошук контактів")
    print("4. Зберегти дані")
    print("5. Завантажити дані")
    print("6. Вийти")

    choice = input("Виберіть опцію: ")

    if choice == '1':
        name = Name.validate_name(input("Введіть ім'я: "))
        if name == 'вийти':
            print('Операція додавання контактів зупинена')
            continue
        while name == False:
            name = Name.validate_name(input("Введіть ім'я: "))
            if name == 'вийти':
                print('Операція додавання контактів зупинена')
                break

        phone = Phone.validate_phone_number(input("Введіть номер телефону: "))
        if phone == 'вийти':
            print('Операція додавання контактів зупинена')
            continue
        while phone == False:
            phone = Phone.validate_phone_number(input("Введіть номер телефону: "))
            if phone == 'вийти':
                print('Операція додавання контактів зупинена')
                break

        email = Email.validate_email(input("Введіть email: "))
        if email == 'вийти':
            print('Операція додавання контактів зупинена')
            continue
        while email == False:
            email = Email.validate_email(input("Введіть email: "))
            if email == 'вийти':
                print('Операція додавання контактів зупинена')
                break


        birthday = Birthday.validate_data(input("Введіть дату народження: "))
        if birthday == 'вийти':
            print('Операція додавання контактів зупинена')
            continue
        while birthday == False:
            birthday = Birthday.validate_data(input("Введіть дату народження: "))
            if birthday == 'вийти':
                print('Операція додавання контактів зупинена')
                break

        address_book.add_record(Record(name, phone, email, birthday))

    if choice == '2':
        print("1. Змінити імя")
        print("2. Змінити номер телефону")
        print("3. Змінити email")
        print("4. Змінити дату народження")
        print("5. Назад")

    elif choice == '3':
        query = input("Введіть запит для пошуку: ")
        results = address_book.search_contacts(query)
        if results:
            for contact in results:
                phones = ', '.join(contact.phones)
                emails = ', '.join(contact.emails)
                print(f"Ім'я: {contact.name}, Телефон: {phones}, Email: {emails}, Birthday: {contact.birthday}")
        else:
            print("Контакти не знайдені")

    elif choice == '4':
        filename = input("Введіть назву файлу для збереження: ")
        address_book.save_to_file(filename)
        print("Дані збережено")
    elif choice == '5':
        filename = input("Введіть назву файлу для завантаження: ")
        address_book.load_from_file(filename)
        print("Дані завантажено")
    elif choice == '6':
        break