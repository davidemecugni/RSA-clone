import sympy
import argparse
import sys
import time
import json
from keys.key import Keys


def strtoint(s):
    nums = ["999"]
    s = str(s.encode("utf8"))[2:-1]
    for c in s:
        num = ord(c)
        if int(num) < 1000:
            if int(num) < 100:
                nums.append("0")
            if int(num) < 10:
                nums.append("0")
            nums.append(str(ord(c)))
    return int("".join(nums))


def inttostr(s):
    s = "".join([chr(int(s[i-2]+s[i-1]+s[i])) for i in range(2, len(s), 3)])
    return s[1:]


# Initialize parser
parser = argparse.ArgumentParser(
    description="A program to demonstate the RSA algorithm\nBy Davide Mecugni")

# Adding optional argument
parser.add_argument(
    "-l", "--len", help="Set lenght of generating prime numbers(default 500)")
parser.add_argument("-gk", "--genkeys", action='store_true',
                    help="Generates a private and public key pair")
parser.add_argument("-ik", "--importkeys",
                    help="Imports the keys from a given file")
parser.add_argument("-ek", "--exportkeys",
                    help="Exports the keys in a given file")
parser.add_argument("-ec", "--exportcertificate",
                    help="Exports the public key")
parser.add_argument("-ic", "--importcertificate",
                    help="Imports the public key")
parser.add_argument("-p", "--print", action='store_true',
                    help="Prints all the keys")
parser.add_argument("-pp", "--printpublic",
                    action='store_true', help="Prints the public key")
parser.add_argument("-v", "--verbose", action='store_true',
                    help="Writes all of what is done")
parser.add_argument("-in", "--input", help="Uses a file as input")
parser.add_argument("-out", "--output", help="Uses a file as output")
parser.add_argument("--public", action='store_true',
                    help="Uses the public key")
parser.add_argument("--private", action='store_true',
                    help="Uses the private key")
parser.add_argument("--textinput", action='store_true', help="Uses text as input")
parser.add_argument("--textoutput", action='store_true', help="Uses text as output")
parser.add_argument("-s", "--shell", action='store_true',
                    help="Runs an interactive shell")

args = parser.parse_args()

keys = Keys()

if args.len:
    keys.length = int(args.len)
    if args.verbose:
        print(f"Set lenght of prime numbers p and q set to {args.len}")

if args.genkeys:
    start = time.time()
    keys.generateKeys()
    if args.verbose:
        print(
            f"Done in: {time.time()-start}s, dimention of generating primes 2^{keys.length}")

if args.importkeys:
    try:
        keys.loadKeysFromFile(args.importkeys)
    except FileNotFoundError:
        print("File not found")
        exit()
    if args.verbose:
        print(f"Imported external keys from file: {args.importkeys}")

if args.importcertificate:
    try:
        keys.loadCertFromFile(args.importcertificate)
    except FileNotFoundError:
        print("File not found")
        exit()
    if args.verbose:
        print(
            f"Imported external certificate from file: {args.importcertificate}")

if args.print:
    keys.printKeys()

if args.printpublic:
    print(keys.publicToString())

if args.exportkeys:
    keys.saveToKeysToFile(args.exportkeys)
    if args.verbose:
        print(f"Exported keys in file: {args.exportkeys}")

if args.exportcertificate:
    keys.saveCertToFile(args.exportcertificate)
    if args.verbose:
        print(f"Exported public key in file: {args.exportcertificate}")

if args.input:
    data = ""
    try:
        with open(args.input) as f:
            data = f.read()

    except FileNotFoundError:
        print("File not found")
        exit()

    encrypted_message = None
    if args.private:
        if args.textinput:
            encrypted_message = keys.encryptWithPrivate(strtoint(data))
        else:
            encrypted_message = keys.encryptWithPrivate(int(data))
    elif args.public:
        if args.textinput:
            encrypted_message = keys.encryptWithPublic(strtoint(data))
        else:
            encrypted_message = keys.encryptWithPublic(int(data))
    else:
        print("Select public or private key")
        exit()
    if args.verbose:
        print(f"Encrypted: \n{encrypted_message}")
    if args.output:
        with open(args.output, "w") as f:
            if args.textoutput:
                f.write(inttostr(str(encrypted_message)))
            else:
                f.write(str(encrypted_message))
        if args.verbose:
            print(f"Exported encrypted input in file: {args.output}")

if args.shell and args.importkeys:
    while True:
        try:
            M = input(f"Insert message(max length {keys.getMaxMessageLength()}):")
            if all(c in '0123456789' for c in M):
                m = int(M)
            else:
                m = strtoint(M)
            c = ""
            if input("My key[m] or other key[o]?") == "m":
                if input("Private[s] or public[p]?") == "s":
                    c = keys.encryptWithPrivate(m)
                else:
                    c = keys.encryptWithPublic(m)
            else:
                k = input("Insert first number of the key: ")
                n = input("Insert second number of the key: ")

                if any(c in 'abcdefABCDEF' for c in k):
                    k = int(k, 16)
                else:
                    k = int(k)

                if any(c in 'abcdefABCDEF' for c in n):
                    n = int(n, 16)
                else:
                    n = int(n)

                c = keys.encrypt(m, k, n)

            print(f"Encrypted: {c}")
            if input("Translate[y or n]: ") == "y":
                print(inttostr(str(c)))
        except KeyboardInterrupt:
            exit()

if len(sys.argv) < 2:
    print("Program by Davide Mecugni, -h for help")
