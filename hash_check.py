import os, hashlib, zlib

def integrity(file_path):
    try:
        filename_without_extension, _ = os.path.splitext(file_path)
        hash_filename = f"{filename_without_extension}.hash"
        with open(hash_filename, 'r') as hash_file:
            lines = hash_file.readlines()
            stored_file_path = lines[0].strip()
            stored_hash_value = lines[1].strip()
            stored_signature = lines[2].strip()

            if file_path!= stored_file_path:
                return f"Error: File path mismatch. Expected {stored_file_path}, got {file_path}"

            current_hash_value = compute(file_path)
            if current_hash_value!= stored_hash_value:
                return f"Error: Hash mismatch. Expected {stored_hash_value}, got {current_hash_value}"

            signature_input = (file_path + current_hash_value).encode()
            signature = hashlib.sha3_512(signature_input).hexdigest()
            if signature!= stored_signature:
                return f"Error: Signature mismatch. Expected {stored_signature}, got {signature}"

            return "File integrity verified successfully."
    except FileNotFoundError:
        return f"Error: Hash file not found for {file_path}"
    except Exception as e:
        return f"Error during verification: {str(e)}"

def compute(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            crc32_h = zlib.crc32(content)
            sha3_512_h = hashlib.sha3_512(content + crc32_h.to_bytes((crc32_h.bit_length() + 7) // 8, 'big')).hexdigest()
            return sha3_512_h
    except FileNotFoundError:
        return None

if __name__ == '__main__':
    file_path = input('Enter a file path: ')
    result = integrity(file_path)
    print(result)