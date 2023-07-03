
import re
import datetime
import os
import pandas as pd
import hashlib
import magic
import mimetypes
import time

log_path = "setupapi.dev2.log"
usb_device_list = []

# Read the contents of the setupapi.dev.log file
with open(log_path, "r") as log_file:
     # Store information about each USB device in a dictionary
     for line in log_file:
        match = re.match('^>>>  \[Device Install.*#(Disk&Ven_[A-Za-z0-9]+)&(Prod_([\w\s\S]+?))&(Rev_([\w\s\S]+?))#([\w\s\S]+?)#.*\]', line)
        if match:
            vendor_id = match.group(1)
            product_id = match.group(2)
            instance_id = match.group(3)
            serial_number = match.group(6)
            line = next(log_file)
            event_line = line.split("t")
            event_time = event_line[3]
            usb_device = {
                "device_vendor_id": vendor_id,
                "device_product_id": product_id,
                "device_instance_id": instance_id,
                "event_time": event_time
            }
            usb_device_list.append(usb_device)
     # Find all USB device installation events and extract information about each device

print(usb_device_list)
print("\n")
# T3R3o5ica#

# ZADATAK 2 -> COPY-PASTE IZ PROSLE VJEZBE

pd.set_option('display.max_columns', None)

# specify the directory path where the files are located
dir_path = './usb'

# create an empty list to store the file names
file_names = []
extensions = []
md5s = []
sha1s = []
sha256s = []
magic_numbers = []
extension_matches = []
creation_times = []
modification_times = []
access_times = []

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

            # izracun MAC vremena
            creation_time = time.ctime(os.path.getctime(dir_path + '/' + file))
            modification_time = time.ctime(os.path.getmtime(dir_path + '/' + file))
            access_time = time.ctime(os.path.getatime(dir_path + '/' + file))

            creation_times.append(creation_time)
            modification_times.append(modification_time)
            access_times.append(modification_time)
            
    # create a Pandas dataframe with the file names
    df = pd.DataFrame({'file_name': file_names, 'extension': extensions, 'md5': md5s, 'sha1': sha1s, 'sha256': sha256s, 'magic_number': magic_numbers, 'extension_match': extension_matches, "creation_time": creation_times, 'modification_time': modification_times, "access_time": access_times})

    return df

print(inspect_directory(dir_path))
