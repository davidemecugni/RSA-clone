import random
import secrets
import math

# Generate a secure random seed
secure_seed = secrets.randbelow(1 << 128)  # Generate a random integer between 0 and 2^32 - 1

# Set the seed for the random module
random.seed(secure_seed)

import sympy

class Keys:
    def __init__(self, private=0, public=0, e = 65537, length=1028):
        self.length = length
        self.e = e
        self.private = private
        self.public = public

    def generateKeys(self):
        p, q = sympy.randprime(
            (2**self.length), (2 * 2**self.length)), sympy.randprime((2**self.length), 2 * (2**self.length))
        n = p * q
        totient_n = (p-1)*(q-1)
        while sympy.gcd(self.e, totient_n) != 1 and self.e < totient_n:
            self.e += 1
        if self.e >= totient_n:
            print("Error in finding e")
            exit()

        public_key = (self.e, n)
        d = sympy.mod_inverse(self.e, totient_n)
        if d < 0:
            print("Error in finding d")
            exit()
        private_key = (d, n)
        self.private = private_key
        self.public = public_key
        self.n = n

    def keysToString(self):
        s = ""
        s += self.publicToString()
        s += self.privateToString()
        return s

    def publicToString(self):
        return self.keyToString(self.public, "PUBLIC")

    def privateToString(self):
        return self.keyToString(self.private, "PRIVATE")
    
    def numberToHex(self, n):
        return hex(n)[2:].upper()
    
    def keyToString(self, key, type):
        s = f"*** START {type} KEY RSA{self.length}***\n"
        s += f"{self.numberToHex(key[0])}\n"
        s += f"{self.numberToHex(key[1])}\n"
        s += f"*** END {type} KEY ***\n"
        return s

    def printKeys(self):
        print(self.keysToString())
    
    def saveToKeysToFile(self, filename):
        with open(filename, "w") as f:
            f.write(self.keysToString())
    
    def saveCertToFile(self, filename):
        with open(filename, "w") as f:
            f.write(self.publicToString())
    
    def savePrivateKeyToFile(self, filename):
        with open(filename, "w") as f:
            f.write(self.privateToString())
    
    def loadKeyFromString(self, s, type):
        start = f"*** START {type} KEY RSA{self.length}***"
        end = f"*** END {type} KEY ***"
        start_index = s.find(start)
        end_index = s.find(end)
        if start_index == -1 or end_index == -1:
            return None
        start_index += len(start)
        s = s[start_index:end_index]
        s = s.split("\n")
        s = [x for x in s if x]
        return (int(s[0], 16), int(s[1], 16))
        
        
    def loadKeysFromString(self, filename):
        self.loadCertFromFile(filename)
        self.loadPrivateKeyFromFile(filename)

    def loadCertFromFile(self, filename):
        self.public = self.loadKeyFromFile(filename, "PUBLIC")

    def loadPrivateKeyFromFile(self, filename):
        self.private = self.loadKeyFromFile(filename, "PRIVATE")

    def loadKeyFromFile(self, filename, type):
        with open(filename, "r") as f:
            return self.loadKeyFromString(f.read(), type)
        
    def loadKeysFromFile(self, filename):
        self.loadCertFromFile(filename)
        self.loadPrivateKeyFromFile(filename)
        
    def encrypt(self, message, key, number):
        if(message > number):
            print("Message too long")
            exit()
        return pow(message, key, number)
    
    def encryptWithPublic(self, message):
        return self.encrypt(message, self.public[0], self.public[1])
    
    def encryptWithPrivate(self, message):
        return self.encrypt(message, self.private[0], self.private[1])

    def getMaxMessageLength(self):
        return round(math.log(self.private[1], 1000) - 1)


if __name__ == "__main__":
    key = Keys()
    key.loadKeysFromFile("short.key")
    