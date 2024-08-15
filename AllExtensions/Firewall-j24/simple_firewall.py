import socket

def main():
    # Soket oluşturma
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 9999))  # 9999 numaralı portu dinle
    s.listen(5)
    
    print("[*] Listening on 0.0.0.0:9999")
    
    while True:
        # Bağlantıyı kabul etme
        client_socket, addr = s.accept()
        print("[*] Accepted connection from:", addr)
        
        # Gelen veriyi alıp işleme
        request = client_socket.recv(1024)
        print("[*] Received:", request.decode())  # Gelen veriyi ekrana yazdırma
        
        # Bağlantıyı kapatma
        client_socket.close()

if __name__ == "__main__":
    main()
