import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 2048
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def main():
    try:
        entrance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        entrance.bind((HOST, PORT))
        entrance.listen()

        print("=== HTTP Server Initiated ===")
        print(f"Base directory: {DIRECTORY}")

        while True:
            (clientSocket, clientAddress) = entrance.accept()

            threadClient = threading.Thread(target=handle_client, args=(clientSocket, clientAddress))
            threadClient.daemon = True
            threadClient.start()
    
    except Exception as e:
        print(f"Error: {e}")

    finally:
        entrance.close()
    
def handle_client(clientSocket, clientAddress):
    print(f"[{clientAddress[0]}:{clientAddress[1]}]: connected")

    try:
        request = clientSocket.recv(4096).decode("utf-8")
        if not request: return

        headers = request.split("\n")
        first_line = headers[0]

        try:
            parts = first_line.split()
            path = parts[1]

            if path == "/":
                filename = "index.html"
            else:
                filename = path[1:]

            print(f"[Requisition] File: {filename}")
            filepath = os.path.join(DIRECTORY, filename)

            if os.path.exists(filepath) and os.path.isfile(filepath):
                filesize = os.path.getsize(filepath)
                content_type = get_content_type(filename)
                
                response_header = [
                    "HTTP/1.1 200 OK",
                    f"Content-Type: {content_type}",
                    f"Content-Length: {filesize}",
                    "Connection: close",
                    "\r\n"
                ]
                
                clientSocket.send("\r\n".join(response_header).encode("utf-8"))

                with open(filepath, 'rb') as f:
                    while True:
                        chunk = f.read(4096)
                        if not chunk: break
                        clientSocket.sendall(chunk)
                
                print(f"[200 OK] Sent: {filename}")
            
            else:
                print(f"[404] Not Found: {filename}")
                
                filepath_404 = os.path.join(DIRECTORY, "404.html")

                if os.path.exists(filepath_404):
                    with open(filepath_404, 'rb') as f:
                        error_content = f.read()
                else:
                    error_content = "<h1>Error 404</h1><p>Not Found</p>".encode("utf-8")
                
                response_header = [
                    "HTTP/1.1 404 Not Found",
                    "Content-Type: text/html",
                    f"Content-Length: {len(error_content)}",
                    "Connection: close",
                    "\r\n"
                ]
                
                clientSocket.send("\r\n".join(response_header).encode("utf-8"))
                clientSocket.sendall(error_content)

        except IndexError:
            pass

    except Exception as e:
        print(f"Error: {e}")

    finally:
        clientSocket.close()
        print(f"[{clientAddress[0]}:{clientAddress[1]}]: connection closed")

def get_content_type(filename):
    if filename.endswith(".html") or filename.endswith(".htm"):
        return "text/html"
    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
        return "image/jpeg"
    else:
        return "application/octet-stream"
 
if __name__ == "__main__":
    main()