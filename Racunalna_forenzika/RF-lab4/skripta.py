import os, sys, optparse
from exif import Image
import webbrowser
from pypdf import PdfReader, PdfWriter

def convertGPScoordinate(coordinate, coordinate_ref):
    decimal_degrees = coordinate[0] + \
                      coordinate[1] / 60 + \
                      coordinate[2] / 3600
    
    if coordinate_ref == "S" or coordinate_ref == "W":
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

def figMetaData(file_path):
    img_doc = Image(open(file_path, "rb"))

    if not img_doc.has_exif:
        sys.exit(f"Image does not contain EXIF data.")
    else:
        print(f"Image contains EXIF (version {img_doc.exif_version}) data.")
        dec_degree_long = convertGPScoordinate(img_doc.gps_longitude, img_doc.gps_longitude_ref)
        dec_degree_lat = convertGPScoordinate(img_doc.gps_latitude, img_doc.gps_latitude_ref)

        coordinates = []
        coordinates.append(dec_degree_long)
        coordinates.append(dec_degree_lat)
        print(coordinates)
        
    print(f"{dir(img_doc)}\n")

    return coordinates


def pdfMetaData(file_path):
    pdf_doc = PdfReader(open(path, "rb"))
    if pdf_doc.is_encrypted:
        pdf_doc.decrypt("PASSWORD_GOES_HERE")

    pdfWriter = PdfWriter()
    for pageNum in pdf_doc.pages:
        pdfWriter.add_page(pageNum)
    with open('decrypted_output.pdf', 'wb') as f:
        pdfWriter.write(f)


if __name__ == "__main__":
    parser = optparse.OptionParser("Usage: python <script_name> -f <file>")
    parser.add_option("-f", dest="file", type="string", help="please provide full path to the document")

    (options, args) = parser.parse_args()

    path = options.file
    if not path:
        print("please provide full path to the document")
        sys.exit(parser.usage)

    if any(path.endswith(ext) for ext in (".jpg", ".bmp", ".jpeg",)):
        coordinates = figMetaData(path)
    elif path.endswith(".pdf"):
        pdfMetaData(path)
    else:
        print("File extension not supported/recognized... Make sure the file has the correct extension...")

    webbrowser.open_new_tab(f"http://www.google.com/maps/place/{coordinates[1]},{coordinates[0]}")