import gzip
import zlib
import rncryptor  # https://github.com/RNCryptor/RNCryptor



password_file = "passwords.txt"
seb_file = "test/session-JREQDV.seb"


# Modify the rncryptor post_decrypt_data class to fit the algorithm
class RNCryptor_modified(rncryptor.RNCryptor):
    def post_decrypt_data(self, data):
        data = data[:-(data[-1])]
        return data

def decrypt_SEB(password):
    cryptor = RNCryptor_modified()
    try:
        with gzip.open(seb_file, 'rb') as f:
            file_content = f.read()
        print(password)
        decrypted_data = cryptor.decrypt(file_content[4:], password)
        decompressed_data = zlib.decompress(decrypted_data, 15 + 32)
        
        with open("decrypted.seb", "wb") as f:
            f.write(decompressed_data)
        print(f"Password found: {password}")
        return True
    except Exception as e:
        return False

def brute_force_password(password_file):
    with open(password_file, 'r') as file:
        for password in file:
            password = password.strip()  # Remove any leading/trailing whitespace
            if decrypt_SEB(password):
                break


brute_force_password(password_file)
