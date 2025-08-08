
import socket
import ssl

host = 'www.google.com'
port = 443

context = ssl.create_default_context()

with socket.create_connection((host, port)) as client_socket:
    with context.wrap_socket(client_socket, server_hostname=host) as secure_socket:
        request = (
            "GET / HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "User-Agent: SecureClient/1.0\r\n"
            "Connection: close\r\n\r\n"
        )
        secure_socket.sendall(request.encode())
        response = b""
        while True:
            chunk = secure_socket.recv(4096)
            if not chunk:
                break
            response += chunk

split_index = response.find(b"\r\n\r\n")
html_content = response[split_index + 4:] if split_index != -1 else response

with open("response.html", "wb") as file:
    file.write(html_content)

print("Saved response to response.html")

