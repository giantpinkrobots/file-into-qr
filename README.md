# File into QR
Encodes/decodes a file into/from a bunch of QR codes
# Why?
I don't know. I would love to hear a good usage for this.
# Usage
You need Python, and the following bits:
- To encode:
  - [qrcode (from pip)](https://pypi.org/project/qrcode/)
- To decode:
  - [pyzbar (from pip)](https://pypi.org/project/pyzbar/)
  - [zbar](http://zbar.sourceforge.net/)

Depending on which functionality you need (just encode or decode), you can skip the dependencies that you don't need.

After the dependencies have been sorted out, you need a (preferably empty) folder for the QR codes. If you're going to encode a file, just create an empty directory. If you're going to decode, then paste all of the qr code images into that directory. Afterwards, you can just run the program like this:
```
python3 ./file-into-qr.py
```
Running the program without any arguments will bring up a series of questions for you to encode or decode a file:
- First, you'll provide the file that you want to encode. If you want to decode, enter the file name that will be created.
- Second, you'll provide the folder that the QR codes will be created in or read from.
- Third, you'll be given the choice between encoding (e) or decoding (d).
- Finally, if you want to encode, you'll be given the option to include the modify date of the file inside one extra QR code. (y/n)

Alternatively, you can run the program with certain arguments to skip this wizard. This can be useful if you want to incorporate it into a script. You can see these arguments by typing:
```
python3 ./file-into-qr.py -h
```
For example, the encode arguments can be like this:
```
python3 ./file-into-qr.py --encode --file myfile.zip --folder qrfolder
```
You can add the additional arguments, too:
- "--date" or "-t" will encode the modify date in one extra QR code.
- "--silent" or "-s" will enable silent mode, so the program will not print any statements besides errors.

At the end of an encode, you will have a folder filled with QR codes with the names "qrX.jpg", where X is the number of the file. Each QR code hold 2214 bytes of information stored in base64. At the end of a decode, you will have the file with the given name generated from the QR codes.

The QR codes inside the folder must keep their names in the same way, since when decoding, the program reads the codes starting from "qr0.jpg" one by one until it reaches the end. At least for now. I'd like to change this behavior and make it better in the future, but I don't know if or when.
