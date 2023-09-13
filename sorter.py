import shutil
from os import *
import sys

# |------------------------------------------------------------------|
# |Sorter('input_folder').sort_files('input_folder', 'output_folder')|
# |------------------------------------------------------------------|

class Sorter:
    def __init__(self, basic_folder):
        self.basic_folder = basic_folder

    def sort_files(self, folder : str, outfolder : str)->None:
        """
        The function sorting all files in folder
        folder(str) - from where the files will be sorted
        outfolder(str) - folder where files will be sorted
        """
        self.create_folders(outfolder)
        try:
            if listdir(folder) == []:
                rmdir(folder)
                self.sort_files(self.basic_folder, outfolder)
            else:
                for el in listdir(folder):
                    if path.isfile(f'{folder}/{el}') == True:
                        file_name = el.split('.')[0]
                        file_exp = el.split('.')[1]
                        if file_exp in ['jpeg', 'png', 'jpg', 'svg']:
                            self.copy_delete_file(folder, file_name, file_exp, 'images', outfolder)
                            self.delele_folder(folder, outfolder)
                        elif file_exp in ['avi', 'mp4', 'mov', 'mkv']:
                            self.copy_delete_file(folder, file_name, file_exp, 'video', outfolder)
                            self.delele_folder(folder, outfolder)
                        elif file_exp in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
                            self.copy_delete_file(folder, file_name, file_exp, 'documents', outfolder)
                            self.delele_folder(folder, outfolder)
                        elif file_exp in ['mp3', 'ogg', 'wav', 'amr']:
                            self.copy_delete_file(folder, file_name, file_exp, 'audio', outfolder)
                            self.delele_folder(folder, outfolder)
                        elif file_exp in ['zip', 'gz', 'tar']:
                            self.copy_delete_file(folder, file_name, file_exp, 'archives', outfolder)
                            self.unpack_archv(f'archives/{self.normalize(file_name)}.{file_exp}', self.normalize(file_name), outfolder)
                            remove(f'{outfolder}/archives/{file_name}.{file_exp}')
                            self.delele_folder(folder, outfolder)
                        else:
                            self.copy_delete_file(folder, file_name, file_exp, 'other', outfolder)
                            self.delele_folder(folder, outfolder)
                    else:
                        self.sort_files(f'{folder}/{el}', outfolder)
        except FileNotFoundError:
            pass

    def unpack_archv(self, folder : str, path_to_unpack : str, outfolder : str)->None:
        """
        The function unpack archives
        folder(str) - folder where is archive
        path_to_unpack - folder where archive will be unpacked
        outfolder(str) - folder where files will be sorted
        """
        mkdir(f"{outfolder}/archives/{path_to_unpack}")
        try:
            shutil.unpack_archive(folder, path_to_unpack)
        except shutil.ReadError:
            pass

    def copy_delete_file(self, folder : str, file_name : str, file_exp : str, out_folder : str, outfolder : str)->None:
        """
        The function copy and delete files
        folder(str) - folder where files
        file_name(str) - name file which will be  copy on the new folder and delete in old folder
        file_exp(str) - file extension
        out_folder(str) - folder where will be file
        outfolder(str) - folder where files will be sorted
        """
        shutil.copy(f'{folder}/{file_name}.{file_exp}', f'{outfolder}/{out_folder}/{self.normalize(file_name)}.{file_exp}')
        remove(f'{folder}/{file_name}.{file_exp}')

    def delele_folder(self, folder : str, outfolder : str)->None:
        """
        The function delete folders
        folder(str) - the folder which will be deleted
        outfolder(str) - folder where files will be sorted
        """
        if listdir(folder) == []:
            rmdir(folder)
            self.sort_files(self.basic_folder, outfolder)

    def create_folders(self, outfolder : str)->None:
        """
        The function creating folders for sorting
        outfolder(str) - folder where files will be sorted
        """
        try:
            mkdir(outfolder)
            mkdir(f'{outfolder}/images')
            mkdir(f'{outfolder}/documents')
            mkdir(f'{outfolder}/audio')
            mkdir(f'{outfolder}/video')
            mkdir(f'{outfolder}/archives')
            mkdir(f'{outfolder}/other')
        except:
            pass

    def normalize(self, name : str)->None:
        """
        The function converts cyrillic characters to latin and characters to _
        name(str) - file name to convert
        Examples:
        файл_1 -> file_1
        файл*_2 -> file__2
        """
        ret_name = str()
        CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
        TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
        TRANS = {}

        for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
            TRANS[ord(c)] = l
            TRANS[ord(c.upper())] = l.upper()

        for el in name.translate(TRANS):
            if not el in TRANSLATION and not el in '0123456789':
                ret_name += '_'
            else:
                ret_name += el
        return ret_name

def main():
    while True:
        try:
            print('If you want exit: exit')
            inp_fold = input("Enter folder that sort: ")
            if inp_fold.lower() == 'exit':
                break
            out_fold = input("Enter output folder: ")
            Sorter(inp_fold).sort_files(inp_fold, out_fold)
            print(f"Files was sorted here:{out_folder}")
        except:
            print('Error')
        
main()