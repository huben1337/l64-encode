import argparse
import os
import hashlib
_lut3 = [ 0x14, 0x0B, 0x09, 0x02, 0x08, 0x03, 0x03, 0x03 ]
_lut4 = [ 0x06, 0x10, 0x0C, 0x02, 0x09, 0x03, 0x04, 0x04, 0x09, 0x05, 0x04, 0x02, 0x05, 0x08, 0x09, 0x15 ]
elif_num = 0
pb_num = 0
#encode file
def EncodeFile(src, dest, overwrite):
    global elif_num
    global pb_num
    print('Processing {0}...'.format(src))
    try:
        with open(src, 'rb') as f:
           srcFile = bytearray(f.read())
    except FileNotFoundError:
        print('File "{0}" not found.'.format(src))
        return
    except:
        print('Failed to read file "{0}".'.format(src))
        return
    poss = 1
    bytes = []
    for i in range(0 , len(srcFile)):
        if i >= ((256 * poss) - (_lut3[i & 0x07])):
            poss += 1
        elif i <= ((256 * (poss - 1)) - (_lut3[i & 0x07])):
            poss -= 1
            elif_num += 1
        for j in range((poss - 2) , (poss + 1)):
            possbyte = (srcFile[i] + (256 * j) - (i + _lut3[i & 0x07]))
            pb_num += 1
            if possbyte >= 0 and possbyte <= 255:
                bytes.append(possbyte)
    bytes[0] = 0x1B
    bytes[1] = 0x4C
    bytes[2] = 0x4A
    bytes[3] = 0x03
    print("hash:", hashlib.sha256(bytearray(bytes)).hexdigest())
    if os.path.isdir(dest):
        fullDestPath = os.path.join(dest, os.path.splitext(os.path.split(src)[1])[0] + '.l64')
    else:
        fullDestPath = dest
    try:
        with open(fullDestPath, 'wb' if overwrite else 'xb') as f:
            f.write(bytearray(bytes))
    except FileExistsError:
        print('The file "{0}" already exists. To overwrite, please specify the -o command line argument.'.format(fullDestPath))
        return
    except:
        print('Could not open file "{0}" for writing.'.format(fullDestPath))
        return
    
#call EncodeFile on every file in a folder 
def EncodeFolder(src, subpath, dest, ext, recursive, overwrite):
    srcDir = os.path.join(src, subpath)
    destDir = os.path.join(dest, subpath)
    os.makedirs(destDir, exist_ok=True)
    with os.scandir(srcDir) as dir:
        for path in dir:
            if path.name.endswith(ext):
                EncodeFile(os.path.join(srcDir, path.name), destDir, overwrite)
            elif recursive and path.is_dir():
                EncodeFolder(src, os.path.join(subpath, path.name), dest, ext, recursive, overwrite)
                
                
#arugment stuff
parser = argparse.ArgumentParser(prog='l64encode.py')
parser.add_argument('input', help='The input filename or folder. If a folder is specified, the program encodes all files in the folder.')
parser.add_argument('output', help='The output filename or folder.')
parser.add_argument('extension', help='The file extension a file must have to be encoded.')
parser.add_argument('-r', '--recursive', action='store_true', help='Recursively encode files in the specified folder and all subdirectories.')
parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite destination file(s) if they already exist.')
args = parser.parse_args()
            
#check wheter its a file or folder and call the corosponding function
if os.path.isfile(args.input):
    EncodeFile(args.input, args.output, args.overwrite)
else:
    EncodeFolder(args.input, '', args.output, args.extension, args.recursive, args.overwrite)

print("elif exec:", elif_num)
print("possbyte set:", pb_num)
print('Done!')