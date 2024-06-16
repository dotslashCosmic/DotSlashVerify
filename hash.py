import os, hashlib, zlib, sys

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
        full_hash = hashlib.sha3_512(str(file_path).encode() + str(hash_value).encode()).hexdigest()
        with open(hash_filename, 'w') as hash_file:
            hash_file.write(f"{file_path}\n{hash_value}\n{full_hash}")
        print(f'Hash created: {hash_filename}')
        sys.exit(1)
    except Exception as e:
        return f'Error during file creation: {str(e)}'

def verify_hash_file(hash_filename):
    try:
        with open(hash_filename, 'r') as hash_file:
            lines = hash_file.readlines()
            file_path = lines[0].strip()
            stored_hash_value = lines[1].strip()
            stored_full_hash = lines[2].strip()
            full_hash = hashlib.sha3_512(str(file_path).encode() + stored_hash_value.encode()).hexdigest()
            if full_hash == stored_full_hash:
                current_hash_value = compute_file_hash(file_path)
                if current_hash_value == stored_hash_value:
                    print(f'Hash verified: {hash_filename}')
                    sys.exit(1)
                else:
                    print(f'Hash mismatch for file: {file_path}')
                    sys.exit(1)
            else:
                print(f'Hash mismatch for hash file: {hash_filename}')
                sys.exit(1)
    except FileNotFoundError:
        print(f'Hash file not found: {hash_filename}')
        sys.exit(1)
    except Exception as e:
        print(f'Error during verification: {str(e)}')
        sys.exit(1)
        
if __name__ == '__main__':
    while True:
        choice = input("Enter 'c' to create hash, 'v' to verify hash, or 'q' to quit: ")
        if choice == 'c':
            file_path = input('Enter a file path: ')
            hash_value = compute_file_hash(file_path)
            if hash_value is not None:
                create_hash_file(file_path, hash_value)
            else:
                print('File not found.')
                sys.exit(1)
        elif choice == 'v':
            filename = input('Enter the hash file path: ')
            filename, _ = os.path.splitext(filename)
            hash_filename = f"{filename}.hash"
            verify_hash_file(hash_filename)
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please enter 'c', 'v', or 'q'.")
