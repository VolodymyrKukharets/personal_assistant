import time
import os
from address_book import main as adress_book
from notes import main as notes
from sorter import main as sorter

def main():
    while True:
        print("1. Адресна книга")
        print("2. Нотатки")
        print("3. Сортування файлів")
        print("4. Вихід")

        command = input("Введіть ваше значення: ")

        if command == "1":
            os.system('cls')
            adress_book()

        elif command == "2":
            os.system('cls')
            notes()

        elif command == "3":
            os.system('cls')
            sorter()

        elif command == "4":
            print("Допобачення!")
            time.sleep(2)
            os.system('cls')
            break

        else:
            print("Некорректне значення, спробуйте ще раз")

if __name__ == "__main__":
    main()