from Crypto.Cipher import DES3
def encrypt(filename,key):
    key = key.encode()
    while True:
        try:
            key = DES3.adjust_key_parity(key)
            break
        except ValueError:
            pass
    with open(filename, "rb") as fIn:
        cipher = DES3.new(key, DES3.MODE_CFB)
        msg = cipher.nonce + cipher.encrypt(fIn.read())
        return msg
def decrypt(filename, data, key):
    key = key.encode()
    key = DES3.adjust_key_parity(key)
    cipher = DES3.new(key, DES3.MODE_CFB)
    msg=cipher.decrypt(data)
    with open(filename,'wb') as fout:
        fout.write(msg)
if __name__ == '__main__':
    edata = encrypt("id.jpeg", "kansal123")
    decrypt('temp.jpeg',edata,'kansal123')