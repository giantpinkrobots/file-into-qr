import argparse # To parse command line arguments

# <Parse command line arguments>
argumentparser = argparse.ArgumentParser()
argumentparser.add_argument("-e","--encode", action='store_true', help="Encode mode")
argumentparser.add_argument("-d","--decode", action='store_true', help="Decode mode")
argumentparser.add_argument("-i","--file", type=str, help="The file name")
argumentparser.add_argument("-f","--folder", type=str, help="The folder that the QR codes will be saved to or read from")
argumentparser.add_argument("-t","--date", action='store_true', help="Save the file's modify date in one extra QR code")
argumentparser.add_argument("-s","--silent", action='store_true', help="Silent mode, don't output anything other than errors")
arguments = argumentparser.parse_args()
# </Parse command line arguments>

includemodifydate = "" # The decision of including or excluding the modify date information will be held in this variable

# <Process the given arguments>
if (arguments.encode and arguments.decode):
    print ("Please choose either encode or decode mode.")
    quit()

if (arguments.encode or arguments.decode):
    if not(arguments.folder or arguments.file):
        print ("Missing arguments.")
        quit()
    if (arguments.encode):
        encodeordecode = "e"
    else:
        encodeordecode = "d"
    main_file = arguments.file
    qrcodes_dir = arguments.folder
    if (arguments.date):
        includemodifydate = "y"
    else:
        includemodifydate = "n"
# </Process the given arguments>

# <If no arguments were given>
else:
    main_file = input("File name: ")
    qrcodes_dir = input("Images directory: ")
    encodeordecode = input("Encode or decode? (e/d): ").lower()
# </If no arguments were given>

qrcode_count = 0 # Counter variable

from os import path # To do a lot of things, can't bother explaining it all tbh
if not (path.isdir(qrcodes_dir)): # Check if folder exists
    print ("Folder does not exist.")
    quit()

# <Encode mode>
if encodeordecode == ('e'):

    # <Include the modify date or not>
    if (includemodifydate == ""): # If the user used the wizard instead of command line arguments
        includemodifydate = input("Encode modify date? (Will use one extra QR code) (y/n): ").lower()
    if includemodifydate == 'y':
        includemodifydate = 1
    elif includemodifydate == 'n':
        includemodifydate = 0
    # </Include the modify date or not>

    # <QR code setup>
    import qrcode
    qr = qrcode.QRCode (
        version = 40,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 2,
        border = 1
    )
    # </QR code setup>

    # <Calculate the amount of QR codes that'll be needed>
    # File will be split into 2214 byte pieces
    qrcode_totalcount = (int(path.getsize(main_file) / 2214))
    if float(qrcode_totalcount) < (path.getsize(main_file) / 2214):
        qrcode_totalcount += 1
    # </Calculate the amount of QR codes that'll be needed>

    if not (arguments.silent):
        if (includemodifydate == 1):
            print ("Encoding into "+str(qrcode_totalcount)+" + 1 (for modify date information) QR codes") # Show start message
        else:
            print ("Encoding into "+str(qrcode_totalcount)+" QR codes") # Show start message
        print ("0 / "+str(qrcode_totalcount+includemodifydate), end='\r') # Print progress

    # <Encode the file into QR codes>
    from base64 import b64encode
    with open(main_file, 'rb') as thefile: # Open the file that will be encoded
        while (qrcode_count < qrcode_totalcount): # Start loop
            encoded = b64encode(thefile.read(2214)) # Convert the 2214 byte section into base64 string
            qr.clear() # Clear the QR code setup
            qr.add_data(encoded) # Add the base64 string into the QR code
            qr.make(fit=True) # Make QR code
            img = qr.make_image(fill_color="black", back_color="white") # Make QR code image with black&white color scheme
            with open(qrcodes_dir+"/qr"+str(qrcode_count)+".png", 'wb') as qrimage: # QR image name will be qr(number).png
                img.save(qrimage) # Save QR code image
            if not (arguments.silent):
                print (str((qrcode_count+1))+" / "+str(qrcode_totalcount+includemodifydate), end='\r') # Print progress
            qrcode_count += 1 # This QR code has been saved, move onto the next 2214 byte section
    # </Encode the file into QR codes>

    # <Encode the modify date into one extra QR code (if the user requested it)>
    if includemodifydate == (1):
        encoded = b64encode(("<!!!modify_date_info>"+str(path.getmtime(main_file))).encode("ascii")) # Convert the modify date of the file into base64 string
        qr.clear() # Clear the QR code setup
        qr.add_data(encoded) # Add the base64 string into the QR code
        qr.make(fit=True) # Make QR code
        img = qr.make_image(fill_color="black", back_color="white") # Make QR code image with black&white color scheme
        with open(qrcodes_dir+"/qr"+str(qrcode_count)+".png", 'wb') as qrimage: # QR image name will be qr(number).png
            img.save(qrimage) # Save QR code image
        if not (arguments.silent):
            print (str((qrcode_count+2))+" / "+str(qrcode_totalcount+includemodifydate), end='\r') # Print progress
    # </Encode the modify date into one extra QR code (if the user requested it)>

    qr.clear() # Clear the QR code setup
    thefile.close() # Close the file
    if not (arguments.silent):
        print ("Encode finished") # Print progress
# </Encode mode>

# <Decode mode>
elif encodeordecode == ('d'):
    from os import listdir # To be able to get the amount of files in given directory
    qrcode_totalcount = ((len(listdir(qrcodes_dir)))-1) # Get total amount of QR codes

    from PIL import Image # To work with image files
    from pyzbar.pyzbar import decode # To use zbar to read QR codes

    if not (arguments.silent):
        print ("Decoding from "+str(qrcode_totalcount+1)+" QR codes") # Show start message
        print ("0 / "+str(qrcode_totalcount+1), end='\r') # Print progress

    # <Decode from QR codes>
    from base64 import b64decode # To decode from base64
    from os import utime
    while (qrcode_count <= int(qrcode_totalcount)): # Start loop
        with open(main_file, 'ab') as thefile: # Open the file that'll be written into
            decoded_data = decode(Image.open(qrcodes_dir+"/qr"+str(qrcode_count)+".png")) # Write base64 read from QR code into the variable "decoded_data"
            if decoded_data: # If the data was successfully decoded
                decoded = b64decode(decoded_data[0].data.decode()) # Decode the base64 string

                # <Deal with modify date information>
                if ((qrcode_count == int(qrcode_totalcount)) and (str(decoded).find("<!!!modify_date_info>") != -1)): # Check if last QR code includes modify date information
                    decoded_date = float("".join(character for character in str(decoded) if (character.isdigit() or character == '.'))) # Remove the "<!!!modify_date_info>" string
                    try:
                        utime(main_file, (decoded_date, decoded_date)) # Write modify date information into the file
                    except:
                        thefile.write(decoded) # Write info into the file
                # </Deal with modify date information>

                else:
                    thefile.write(decoded) # Write info into the file

                thefile.close() # Close the file
                qrcode_count += 1 # Go to the next QR code
                if not (arguments.silent):
                    print (str((qrcode_count+1))+" / "+str(qrcode_totalcount+1), end='\r') # Print progress
    # </Decode from QR codes>

    if not (arguments.silent):
        print ("Decode finished") # Print progress
# </Decode mode>