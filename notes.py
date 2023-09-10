import re
import pickle

FILENAME = "notes.dat"

class Notes:
    # Метод пошуку
    def search_text(records, text):
        # Створюємо порожній список для результатів
        results = []
        # Компілюємо регулярний вираз із тексту
        pattern = re.compile(text)
        # Перебираємо всі записи

        for record in records:
            # Перевіряємо, чи є збіг з регулярним виразом у записі
            if pattern.search(record):
                # Додаємо запис до списку результатів
                results.append(record)
        # Повертаємо перелік результатів
        return results
      
    def save(self, filename):
        # Відкриваємо файл для збереження
        with open(filename, 'wb') as file:
            # зберігаємо серіалізовані дані
            pickle.dump(self, file)  

"""
Функціонал для роботи із записною книгою
Task7
Пошук: Пошку виконується за строкою або за регулярним вираженням залежно від того, що ви хочете знайти. 
Наприклад, якщо ви хочете знайти всі записи, які містять слово "купити", ви можете використовувати текст "купити". 
Якщо ви хочете знайти всі записи, які починаються з літери "А", ви можете використати текст "^A". 
Якщо ви хочете знайти всі записи, які закінчуються на цифру, ви можете використовувати текст "\d$".
Приклад виклику: search_text(records, "купити")

Збереження: Збереження виконується у режимі 'wb', 
тобто відкриває файл як для запису, так читання у двійковому форматі. 
Перезаписує існуючий файл, якщо він існує. 
Якщо файл не існує, створюється новий файл для читання та запису.
При збережені використовується функція dump модуля pickle - записує серіалізований об'єкт у файл. 
Серіалізація - перетворення об'єкта Python на потік байтів.
При виклику методу пропонується використовувати змінну FILENAME.
Приклад виклику: .save(self, "FILENAME")
"""


class Note:
    def __init__(self, content):
        self.content = content


class NoteBook:
    def __init__(self):
        self.notes = []

    def add_note(self, content):
        note = Note(content)
        self.notes.append(note)

    def edit_note(self, index, new_content):
        if 0 <= index < len(self.notes):
            self.notes[index].content = new_content
        else:
            print("Invalid note index.")

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
        else:
            print("Invalid note index.")

    def view_notes(self):
        if not self.notes:
            print("No notes available.")
        else:
            print("Notes:")
            for i, note in enumerate(self.notes):
                print(f"{i + 1}. {note.content}")

def main():
    notebook = NoteBook()

    while True:
        command = input("Enter a command (add/edit/delete/view/exit): ").strip().lower()

        if command == "add":
            content = input("Enter the content of the note: ")
            notebook.add_note(content)
            print("Note added.")

        elif command == "edit":
            index = int(input("Enter the index of the note to edit: "))
            new_content = input("Enter the new content: ")
            notebook.edit_note(index - 1, new_content)
            print("Note edited.")

        elif command == "delete":
            index = int(input("Enter the index of the note to delete: "))
            notebook.delete_note(index - 1)
            print("Note deleted.")

        elif command == "view":
            notebook.view_notes()

        elif command == "exit":
            print("Goodbye!")
            break

        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
