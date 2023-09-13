import time
import os
import pickle


class NoteBook:
    def __init__(self):
        super().__init__()
        self.notes = []

    def edit(self, note):
        """
        Редагувати нотатку в блокноті.
        """
        index = self.notes.index(note)
        print(f"Тег:\n{note.tag}")
        new_tag = input(f"Введіть новий значення тегу: ")
        os.system('cls')
        print(f"Ваша нотатка:\n{note.content}")
        new_content = input(f"Введіть новий текст: ")
        os.system('cls')
        self.notes[index] = NoteTag(new_tag, new_content)
        print(f"Нотатка '{note.tag}' відредагована.")

    def delete(self, note):
        """
        Видалити нотатку з блокнота.
        """
        self.notes.remove(note)
        print(f"Нотатка '{note.tag}' видалена.")

    def save(self):
        """
        Зберегти нову нотатку в блокнот.
        """
        tag = input("Введіть тег для нотатки: ")
        content = input("Введіть зміст для нотатки: ")
        new_note = NoteTag(tag, content)
        self.notes.append(new_note)
        print(f"Нотатка '{tag}' додана.")

    def view(self):
        """
        Переглянути всі нотатки в блокноті.
        """
        if not self.notes:
            print("Немає доступних нотаток.")
        else:
            for index, note in enumerate(self.notes, start=1):
                print(f"{index}. Тег: {note.tag}, Зміст: {note.content}")

    def sort(self):
        """
        Сортувати всі нотатки в блокноті.
        """
        self.notes.sort(key=lambda note: note.tag)
        print("Нотатки відсортовані.")

    def search(self, keyword):
        """
        Пошук нотаток за конкретним ключовим словом в блокноті.
        """
        matching_notes = [note for note in self.notes if keyword in note.tag or keyword in note.content]
        if matching_notes:
            for index, note in enumerate(matching_notes, start=1):
                print(f"{index}. Тег: {note.tag}, Зміст: {note.content}")
        else:
            print("Не знайдено нотаток за вказаним ключовим словом.")


    def save_to_file(self, filename):
        # Перевіряємо, чи існує каталог 'address_book_save'
        if not os.path.exists('notes_save'):
            os.makedirs('notes_save')  # Якщо не існує, створюємо його

        with open(f'notes_save/{filename}', 'wb') as file:
            pickle.dump(self.notes, file)

    def load_from_file(self, filename):
        with open(f'notes_save/{filename}', 'rb') as file:
            self.notes = pickle.load(file)

class NoteTag:
    def __init__(self, tag, content):
        self.tag = tag
        self.content = content

def main():
    notebook = NoteBook()

    while True:
        print("1. Додати нову нотатку")
        print("2. Редагувати нотатку")
        print("3. Видалити нотатку")
        print("4. Переглянути всі нотатки")
        print("5. Сортувати всі нотатки")
        print("6. Пошук нотатки")
        print("7. Зберегти нотатки в файл")
        print("8. Завантажити нотатки з файлу")
        print("9. Вихід")
        command = input("Введіть команду: ")

        if command == "1":
            os.system('cls')
            notebook.save()
            time.sleep(2)
            os.system('cls')

        elif command == "2":
            os.system('cls')
            notebook.view()
            if notebook.notes:
                index = int(input("Введіть номер нотатки для редагування: ")) - 1
                if 0 <= index < len(notebook.notes):
                    notebook.edit(notebook.notes[index])
                else:
                    print('Некорректне значення')
                    time.sleep(2)
                    os.system('cls')

        elif command == "3":
            os.system('cls')
            notebook.view()
            if notebook.notes:
                index = int(input("Введіть номер нотатки для видалення: ")) - 1
                if 0 <= index < len(notebook.notes):
                    notebook.delete(notebook.notes[index])
                else:
                    print('Некорректне значення')
                    time.sleep(2)
                    os.system('cls')

        elif command == "4":
            os.system('cls')
            notebook.view()
            input('Для повернення натисніть Ентер')
            os.system('cls')

        elif command == "5":
            os.system('cls')
            option = input("Всі нотатки будуть відсортовані в алфавітному порядку. Відсортувати? (так/ні): ").strip().lower()
            option = True if option == "так" else False
            if option:
                notebook.sort()
                time.sleep(2)
                os.system('cls')
            else:
                print('Відміна')
                time.sleep(2)
                os.system('cls')


        elif command == "6":
            os.system('cls')
            keyword = input("Введіть ключове слово для пошуку: ")
            notebook.search(keyword)
            input('Для повернення натисніть Ентер')
            os.system('cls')

        elif command == '7':
            os.system('cls')
            filename = input("Введіть назву файлу для збереження: ")
            notebook.save_to_file(filename)
            print("Дані збережено")
            time.sleep(2)
            os.system('cls')

        elif command == '8':
            os.system('cls')
            filename = input("Введіть назву файлу для завантаження: ")
            try:
                notebook.load_from_file(filename)
                print("Дані завантажено")
                time.sleep(2)
                os.system('cls')
            except:
                print("Файл не знайдено")
                time.sleep(2)
                os.system('cls')

        elif command == "9":
            os.system('cls')
            break

        else:
            print("Некоректна команда. Спробуйте ще раз.")
            time.sleep(2)
            os.system('cls')

if __name__ == "__main__":
    main()
