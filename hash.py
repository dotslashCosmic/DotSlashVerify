import os, hashlib, zlib

def compute_file_hash(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            crc32_hash = zlib.crc32(content)
            sha3_512_hash = hashlib.sha3_512(content + crc32_hash.to_bytes((crc32_hash.bit_length() + 7) // 8, 'big')).hexdigest()
            return sha3_512_hash
    except FileNotFoundError:
        return None

def create_hash_file(file_path, hash_value):
    try:
        filename, _ = os.path.splitext(file_path)
        hash_filename = f"{filename}.hash"
        with open(hash_filename, 'w') as hash_file:
            hash_file.write(f'{file_path}\n')
            hash_file.write(f'{hash_value}\n')
            hash_file.write(f'{hashlib.sha3_512((file_path + hash_value).encode()).hexdigest()}')
    except Exception as e:
        return f'Error during file creation: {str(e)}'

if __name__ == '__main__':
    file_path = input('Enter a file path: ')
    hash_value = compute_file_hash(file_path)
    if hash_value is not None:
        create_hash_file(file_path, hash_value)
        print(f'Hash created.')
    else:
        print('File not found.')
