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