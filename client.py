import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

# تابع برای بستن پنجره چت
def close_window():
    send_message("exit")


# تابع برای ارسال پیام
def send_message(message=None):
    if message is None:
        message = message_entry.get()
    if message:
        full_message = f"{username}: {message}"  # نام کاربری فرستنده پیام در ابتدای پیام قرار می‌گیرد
        print('$$$ : ', full_message)
        client_socket.send(full_message.encode('utf-8'))
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, full_message + "\n")  # نمایش پیام و نام کاربری در پنجره چت
        chat_log.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)
        if message == "exit":  # اگر کاربر "exit" را ارسال کند، پنجره چت را ببندید
            root.destroy()

# تابع برای دریافت پیام
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                chat_log.config(state=tk.NORMAL)
                chat_log.insert(tk.END, "Other: has left the chat.\n")
                chat_log.config(state=tk.DISABLED)
                root.destroy()  # بعد از دریافت پیام خالی، پنجره چت را ببندید
            else:
                if "Welcome" in message:  # چک کردن اینکه پیام خوش‌آمدگویی است
                    chat_log.config(state=tk.NORMAL)
                    chat_log.insert(tk.END, f"{message}\n")  # نمایش پیام خوش‌آمدگویی
                    chat_log.config(state=tk.DISABLED)
                else:
                    chat_log.config(state=tk.NORMAL)
                    chat_log.insert(tk.END, f"{message}\n")
                    chat_log.config(state=tk.DISABLED)
        except:
            print("An error occurred!")
            client_socket.close()
            break

# اتصال به سرور
def connect_to_server():
    global client_socket, username
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    username = input("Enter your username: ")
    client_socket.send(username.encode('utf-8'))
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()
    root.title(f"{username} client")

# تعیین HOST و PORT برای اتصال به سرور
HOST = '127.0.0.1'  # آدرس IP محلی
PORT = 55555        # پورت برای اتصال

# ایجاد پنجره
root = tk.Tk()


# ایجاد صفحه چت
chat_log = scrolledtext.ScrolledText(root, state=tk.DISABLED)
chat_log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# ایجاد ورودی پیام
message_entry = tk.Entry(root, width=50)
message_entry.grid(row=1, column=0, padx=10, pady=10)

# ایجاد دکمه ارسال
send_button = tk.Button(root, text="Send", width=10, command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# ایجاد دکمه برای بستن پنجره چت
close_button = tk.Button(root, text="Close", width=10, command=close_window)
close_button.grid(row=2, column=1, padx=10, pady=10)

# اتصال به سرور هنگامی که پنجره باز می‌شود
connect_to_server()

# اجرای پنجره
root.mainloop()
