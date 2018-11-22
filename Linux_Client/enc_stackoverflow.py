import base64
from Crypto import Random

from Crypto.Cipher import AES



class PKCS7Encoder():
    """
    Technique for padding a string as defined in RFC 2315, section 10.3,
    note #2
    """
    class InvalidBlockSizeError(Exception):
        """Raised for invalid block sizes"""
        pass

    def __init__(self, block_size=16):
        if block_size < 2 or block_size > 255:
            raise PKCS7Encoder.InvalidBlockSizeError('The block size must be ' \
                    'between 2 and 255, inclusive')
        self.block_size = block_size

    def encode(self, text):
        text_length = len(text)
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def decode(self, text):
        pad = ord(text[-1])
        return text[:-pad]

def encrypt_val(clear_text):
    master_key = '1234567890123456'
    encoder = PKCS7Encoder()
    raw = encoder.encode(clear_text)
    iv = Random.new().read( 16 )
    cipher = AES.new( master_key, AES.MODE_CBC, iv, segment_size=128 )
    return base64.b64encode( iv + cipher.encrypt( raw ) )

if __name__ == '__main__':
    print(encrypt_val("abc"))