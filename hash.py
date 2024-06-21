# Author:dotslashCosmic
import os, hashlib, zlib, random, time
art = """
COSMIC@' '@@@'   '''     '@''     ''         ''   '@@@'
HASH '@ '@' '@ '@@'@@@' '@      '@@@@''   '@@'@@ '@' '@
96   '@'@'    '@'    '@''@@@@@ '@  '@@@@' '   '@'@'
    '@ '@'    '@      @'    @''@   '@  '@'   '@ '@'
 '  '@ '@'     @'   '@'   '@  @'   '@   '@  '@  '@
'' '@'  '@@''' ''@@@@'    ''  @'   ''   '@  '@   '@@'''
"""
def compute_file_hash(file_path):
    try:
        blake2b_hash = hashlib.blake2b(digest_size=20)
        sha3_512_hash = hashlib.sha3_512()
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(4096)
                if not chunk:
                    break
                blake2b_hash.update(chunk)
                sha3_512_hash.update(chunk)
        return blake2b_hash, sha3_512_hash.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None, None

def create_hash_file(file_path, blake2b_hash, sha3_512_hash):
    try:
        hash_filename = f"{file_path}.hash"
        author = input("Enter author name: ")
        salt = ''.join(filter(lambda x: x not in '@ ', art.split('\n')[1][6:16]))
        sign = hashlib.sha3_512((author + salt).encode()).hexdigest()[:-5]
        cosmichash = list(art)
        cosmichash[14] = sign[0]
        cosmichash[20] = sign[1]
        cosmichash[26] = sign[2]
        cosmichash[29] = sign[3]
        cosmichash[47] = sign[4]
        period_count = 0
        hash_index = 1
        for i in range(len(cosmichash)):
            if cosmichash[i] == "'":
                period_count += 1
                if period_count % 1 == 0:
                    cosmichash[i] = sha3_512_hash[hash_index % len(sha3_512_hash)]
                    hash_index += 3
        for i in range(len(cosmichash) - 1, len(cosmichash)):
            cosmichash[i] = sign[hash_index % len(sign)]
        with open(hash_filename, 'w') as hash_file:
            hash_file.write(author + ''.join(cosmichash))
        print(f'Hash created: {hash_filename}\n{author}', ''.join(cosmichash))
    except Exception as e:
        print(f'Error during file creation: {str(e)}')
        
def validate_hash(file_path):
    try:
        hash_filename = f"{file_path}.hash"
        with open(hash_filename, 'r') as hash_file:
            lines = hash_file.readlines()
            author = lines[0].strip()
            stored_hash = ''.join(lines[1:]).strip()
        blake2b_hash, sha3_512_hash = compute_file_hash(file_path)
        if blake2b_hash is None or sha3_512_hash is None:
            print("File not found or unable to compute hash.")
            return
        salt = ''.join(filter(lambda x: x not in '@ ', art.split('\n')[1][6:16]))
        sign = hashlib.sha3_512((author + salt).encode()).hexdigest()[:-5]
        cosmichash = list(art)
        cosmichash[14] = sign[0]
        cosmichash[20] = sign[1]
        cosmichash[26] = sign[2]
        cosmichash[29] = sign[3]
        cosmichash[47] = sign[4]
        period_count = 0
        hash_index = 1
        for i in range(len(cosmichash)):
            if cosmichash[i] == "'":
                period_count += 1
                if period_count % 1 == 0:
                    cosmichash[i] = sha3_512_hash[hash_index % len(sha3_512_hash)]
                    hash_index += 3
        for i in range(len(cosmichash) - 1, len(cosmichash)):
            cosmichash[i] = sign[hash_index % len(sign)]
        generated_hash = author + ''.join(cosmichash)
        h1 = "".join(generated_hash)
        h2 = "".join(lines)
        if h1 == h2:
            print("Hash is valid.")
        else:
            print("Hash is invalid.")
    except Exception as e:
        print(f'Error during validation: {str(e)}')
        
def main():
    while True:
        try:
            choice = input("Enter 'c' to create hash, 'v' to verify hash, or 'q' to quit: ")
            if choice == 'c':
                file_path = input('Enter a file name: ')
                blake2b_hash, sha3_512_hash = compute_file_hash(file_path)
                if blake2b_hash is not None and sha3_512_hash is not None:
                    create_hash_file(file_path, blake2b_hash, sha3_512_hash)
            elif choice == 'v':
                filename = input('Enter the original file name: ')
                validate_hash(f'{filename}')
            elif choice == 'q':
                break
            else:
                print("Invalid choice. Please enter 'c', 'v', or 'q'.")
        except Exception as e:
            print(f'Error: {str(e)}')

if __name__ == '__main__':
    main()
