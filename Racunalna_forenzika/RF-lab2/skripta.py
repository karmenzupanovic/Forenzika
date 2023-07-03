import os
import pandas as pd
import hashlib
import magic
import mimetypes

pd.set_option('display.max_columns', None)

# specify the directory path where the files are located
dir_path_test = './labovi2'
dir_path_evidence = "./Dokaz"

# target hash
target_hash = "c15e32d27635f248c1c8b66bb012850e5b342119"

# create an empty list to store the file names
file_names = []
extensions = []
md5s = []
sha1s = []
sha256s = []
magic_numbers = []
extension_matches = []

magic_object = magic.Magic(mime = True)

def inspect_directory(dir_path):
    # iterate through all files in the directory
    for file in os.listdir(dir_path):

        # check if the file is a regular file (i.e., not a directory)
        if os.path.isfile(os.path.join(dir_path, file)):
            # if so, add the file name to the list
            file_names.append(file)

            # vjezba 2 - spremanje ekstenzije datoteke u listu
            extension = os.path.splitext(file)[1]
            extensions.append(extension)

            # vjezba 3 - računanje hash vrijednosti datoteka
            with open(os.path.join(dir_path, file), 'rb') as f:
                data = f.read()
                md5 = hashlib.md5(data).hexdigest()
                sha1 = hashlib.sha1(data).hexdigest()
                sha256 = hashlib.sha256(data).hexdigest()
                md5s.append(md5)
                sha1s.append(sha1)
                sha256s.append(sha256)
            
            # vjezba 4 - detekcija vrste datoteke
            magic_number = magic_object.from_file(os.path.join(dir_path, file))
            magic_numbers.append(magic_number)

            # vjezba 5 - provjera odgovara li vrsta datoteke njenoj ekstenziji
            if extension.lower() == '':
                extension_matches.append(False)
            elif mimetypes.guess_type('test'+extension.lower())[0] in magic_number.lower():
                extension_matches.append(True)
            else:
                extension_matches.append(False)

    # create a Pandas dataframe with the file names
    df = pd.DataFrame({'file_name': file_names, 'extension': extensions, 'md5': md5s, 'sha1': sha1s, 'sha256': sha256s, 'magic_number': magic_numbers, 'extension_match': extension_matches})

    return df

def find_stolen_file(dir_path):
    for file in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file)):
            with open(os.path.join(dir_path, file), 'rb') as f:
                data = f.read()
                md5 = hashlib.md5(data).hexdigest()
                sha1 = hashlib.sha1(data).hexdigest()
                sha256 = hashlib.sha256(data).hexdigest()

                if md5 == target_hash or sha1 == target_hash or sha256 == target_hash:
                    return file
    return "The stolen file is not found"            


# print the dataframe
print(inspect_directory(dir_path_evidence))
print("Stolen file: ", find_stolen_file(dir_path_evidence))