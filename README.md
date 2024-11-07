# RSA-clone
A basic RSA implementation in Python. The purpose of this project is to understand the RSA algorithm and how it works. The code is heavily commented to explain the steps of the algorithm.

## How to use
Here is the -help output of the program:
```
usage: app.py [-h] [-l LEN] [-gk] [-ik IMPORTKEYS] [-ek EXPORTKEYS] [-ec EXPORTCERTIFICATE]
              [-ic IMPORTCERTIFICATE] [-p] [-pp] [-v] [-in INPUT] [-out OUTPUT] [--public] [--private]
              [--textinput] [--textoutput] [-s]

A program to demonstate the RSA algorithm By Davide Mecugni

options:
  -h, --help            show this help message and exit
  -l LEN, --len LEN     Set lenght of generating prime numbers(default 500)
  -gk, --genkeys        Generates a private and public key pair
  -ik IMPORTKEYS, --importkeys IMPORTKEYS
                        Imports the keys from a given file
  -ek EXPORTKEYS, --exportkeys EXPORTKEYS
                        Exports the keys in a given file
  -ec EXPORTCERTIFICATE, --exportcertificate EXPORTCERTIFICATE
                        Exports the public key
  -ic IMPORTCERTIFICATE, --importcertificate IMPORTCERTIFICATE
                        Imports the public key
  -p, --print           Prints all the keys
  -pp, --printpublic    Prints the public key
  -v, --verbose         Writes all of what is done
  -in INPUT, --input INPUT
                        Uses a file as input
  -out OUTPUT, --output OUTPUT
                        Uses a file as output
  --public              Uses the public key
  --private             Uses the private key
  --textinput           Uses text as input
  --textoutput          Uses text as output
  -s, --shell           Runs an interactive shell
```