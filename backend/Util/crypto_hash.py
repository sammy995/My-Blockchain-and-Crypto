import hashlib ,json

"""
def stringify(data):
    return json.dumps(data)
LAMBDA function is used to replace above function inline
"""
def crypto_hash(*args):
    """
    Returns a SHA-256 hash of given arguments
    First data needs to be encoded
    JSON dumps allows to convert any input into string to be encoded. Needed as hashlib.sha256 only takes BYTE_STRING as input
    Hex digest is used to get 64 bit hash value instead of address
    """
    stringified_args = sorted (map(lambda data: json.dumps(data), args))
    #print(f'Stringifiedargs : {stringified_args}')
    joined_data = ''.join(stringified_args)
    #print(f'joined_data : {joined_data}')
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"crypto_hash(''one',2,[3]') :{crypto_hash('one',2,[3])}")
    print(f"crypto_hash('2,'one',[3]') :{crypto_hash(2,'one',[3])}")

if __name__ == '__main__':
    main()