import subprocess

OPENSSL_PATH = r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe"

def generate_dh_params(file_path="dhparams.pem", size=2048):
    """
    Chạy lệnh OpenSSL để tạo file Diffie-Hellman parameters với kích thước mong muốn.

    Parameters:
        file_path (str): Đường dẫn file để lưu DH params.
        size (int): Độ dài key (mặc định là 2048 bit).

    Returns:
        bool: True nếu thành công, False nếu có lỗi.
    """
    try:
        # Chạy lệnh OpenSSL để tạo DH parameters
        subprocess.run([OPENSSL_PATH, "dhparam", "-out", file_path, str(size)], check=True)
        print(f"✅ DH parameters đã được tạo thành công và lưu tại: {file_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi tạo DH parameters: {e}")
        return False

# generate_dh_params(f"dhparams.pem", 2048)

# **Chạy chương trình**
for i in range(100):
  generate_dh_params(f"dhparams{i}.pem", 2048)