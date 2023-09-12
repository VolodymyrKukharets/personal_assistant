class NoteBook:
    """
    Class NoteBook responsible for management in the notebook
    """
    def edit(self, index : int, new_content : str):
        """
        The function editing one element in notes
        index(int) - number element which will be changed
        new_content(str) - new content which will be added
        Example:
            notes.txt:
                test1
                test2
                test3
            If we want edit the second element:
            NoteBook().edit(2, 'new text')
        """
        if 1 <= index < len(NoteBook().view()):
            notes = NoteBook().view()
            notes[index-1] = new_content
            with open('notes.txt', 'w', encoding='utf-8') as fl:
                for el in notes:
                    fl.write(f'{el}\n')
            return 'Notes edited'
        else:
            print("Invalid note index.")

    def delete(self, index : int):
        """
        The function delete one element from notes
        index(int) - number element which will be deleted
        Example:
            notes.txt:
                test1
                test2
                test3
            If we want delete the second element:
            NoteBook().delete(2)
        """
        if 1 <= index < len(NoteBook().view()):
            notes = NoteBook().view()
            del notes[index-1]
            with open('notes.txt', 'w', encoding='utf-8') as fl:
                for el in notes:
                    fl.write(f'{el}\n')
            return 'Note deleted'
        else:
            print("Invalid note index.")

    def save(self, content : str):
        """
        The function save new element to notes
        content(str) - new content which will be added
        Example:
            notes.txt:
                test1
                test2
                test3
            If we want add new element:
            NoteBook().save('test4')
            notes.txt:
                test1
                test2
                test3
                test4
        """
        try:
            with open('notes.txt', 'a', encoding='utf-8') as fl:
                fl.write(f'{content}\n')
        except:
            with open('notes.txt', 'w', encoding='utf-8') as fl:
                fl.write(f'{content}\n')

    def view(self):
        """
        The function read notes.txt
        return(list) - list with all notes
        """
        notes = list()
        with open('notes.txt', 'r', encoding='utf-8') as fl:
            for el in fl.readlines():
                notes.append(el.replace('\n', ''))
        return notes

    def sort(self, reverse : bool=False):
        """
        The function sort all notes
        reverse(bool) - if we want the reverse, the default is False
        """
        notes = NoteBook().view()

        with open('notes.txt', 'w', encoding='utf-8') as fl:
            for el in sorted(notes, reverse=reverse):
                fl.write(f'{el}\n')
        return 'Notes sorted'

    def search(self, keyword : str):
        """
        The function search notes for keyword
        keyword(str) - parametr(word which is on note)
        return(list) - list notes with keyword
        """
        notes = NoteBook().view()
        ret_notes = list()

        for el in notes:
            if keyword in el:
                ret_notes.append(el)
        return ret_notes

def main():
    notebook = NoteBook()

    while True:
        command = input("1.Add new note\n2.Edit some note\n3.Delete some note\n4.View all notes\n5.Sort all notes\n6.Search some note\n7.Exit\nEnter a command: ").strip().lower()

        if command == "1":
            content = input("Enter the content of the note: ")
            notebook.save(content)
            print("Note added.")

        elif command == "2":
            index = int(input("Enter the index of the note to edit: "))
            new_content = input("Enter the new content: ")
            notebook.edit(index, new_content)
            print("Note edited.")

        elif command == "3":
            index = int(input("Enter the index of the note to delete: "))
            notebook.delete(index)
            print("Note deleted.")

        elif command == "4":
            try:
                x = 1
                for el in notebook.view():
                    print(f'{x}.{el}')
                    x += 1
            except:
                print("No notes available.")

        elif command == "5":
            reverse_t_f = input("Reverse(y/n): ").lower()
            if reverse_t_f == 'y':
                print(notebook.sort(reverse=True))
            elif reverse_t_f == 'n':
                print(notebook.sort())

        elif command == "6":
            keyword = input("Input keyword: ")
            try:
                x = 1
                for el in notebook.search(keyword):
                    print(f'{x}.{el}')
                    x += 1
            except:
                print("No notes available.")

        elif command == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid command. Please try again.")

main()