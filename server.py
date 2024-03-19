import socket
import threading

# تنظیمات سرور
HOST = '127.0.0.1'  # آدرس IP محلی
PORT = 55555        # پورت برای اتصال

# ذخیره نام کاربری هر کلاینت
clients = {}

# پیام خوش‌آمدگویی
def welcome_message(client):
    username = clients[client]
    return f"Welcome, {username}! Say hello to others."

# ارسال پیام به تمام کلاینت‌ها
def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:  # ارسال به تمام کلاینت‌ها به جز کلاینت فرستنده
            client.send(message)

# پردازش پیام‌ها
def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8') == "exit":
                username = clients[client]
                print(f"{username} has left the chat.")
                client.close()
                del clients[client]
                broadcast(f"{username} has left the chat.".encode('utf-8'), client)  # ارسال پیام خروج به تمام کلاینت‌ها
                break
            broadcast(message, client)
        except:
            username = clients[client]
            print(f"{username} has left the chat.")
            client.close()
            del clients[client]
            broadcast(f"{username} has left the chat.".encode('utf-8'), client)  # ارسال پیام خروج به تمام کلاینت‌ها
            break


# تابع برای ارسال پیام خوش‌آمدگویی به یک کلاینت
def send_welcome_message(client):
    welcome_msg = welcome_message(client)
    client.send(welcome_msg.encode('utf-8'))


# ایجاد اتصال و مدیریت کلاینت‌ها
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server is running...")
    while True:
        client, address = server.accept()
        print(f"Connection from {address} has been established!")

        # client.send("Enter your username: ".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        clients[client] = username

        # فراخوانی تابع برای ارسال پیام خوش‌آمدگویی
        send_welcome_message(client)

        broadcast(f"{username} has joined the chat!".encode('utf-8'), client)

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()
