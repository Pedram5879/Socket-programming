import random
import time

class TCPPacket:
    def __init__(self, sequence_number, ack_number, window_size, rtt):
        self.sequence_number = sequence_number  # شماره دنباله پکت
        self.ack_number = ack_number  # شماره تأیید
        self.window_size = window_size  # اندازه پنجره
        self.rtt = rtt  # زمان Round-Trip Time

def is_congested():
    # تابع برای بررسی وضعیت ازدحام است
    return random.random() < 0.3  # احتمال وقوع ازدحام

def random_packet(rtt):
    # تولید یک پکت تصادفی با مقدار RTT دلخواه
    sequence_number = random.randint(0, 1000)
    ack_number = random.randint(0, 1000)
    window_size = random.randint(1, 100)
    return TCPPacket(sequence_number, ack_number, window_size, rtt)

def tcp_tahoe_congestion_control(window_size):
    # الگوریتم کنترل ازدحام TCP Tahoe
    window_size = max(window_size // 2, 1)  # کاهش نصف اندازه پنجره
    print('Window size after tcp_tahoe_congestion_control', window_size)
    return window_size

def send_packet(packet):
    # ارسال پکت و گزارش وضعیت
    print("Sending packet:", packet.sequence_number, packet.ack_number, packet.window_size, packet.rtt)
    time.sleep(packet.rtt / 1000)  # استفاده از مقدار RTT برای شبیه‌سازی زمان ارسال پکت

def wait_for_ack(wait_time):
    # انتظار برای دریافت تأییدیه و گزارش وضعیت
    print("Waiting for acknowledgment...")
    time.sleep(wait_time)  # شبیه‌سازی زمان انتظار برای دریافت تأییدیه

def receive_ack(increse_window_size_duration):
    # دریافت تأییدیه و افزایش اندازه پنجره
    global window_size  # استفاده از متغیر گلوبال برای اندازه پنجره
    print("Receiving acknowledgment...")
    # دریافت تأییدیه
    time.sleep(increse_window_size_duration)  # شبیه‌سازی زمان دریافت تأییدیه
    # افزایش اندازه پنجره و گزارش وضعیت
    window_size += 1  # افزایش اندازه پنجره به صورت یک واحد
    print("Window size increased to", window_size, "after receiving acknowledgment!")

def timeout_for_packet_loss(timeout_duration):
    # مدیریت زمان اتلاف پکت و گزارش وضعیت
    print("Timeout for packet loss...")
    time.sleep(timeout_duration)  # شبیه‌سازی زمان اتلاف پکت

def initialize_simulation_parameters(t_d, i_w_s_d, w_t, r, w_s):
    # مقداردهی اولیه پارامترهای شبیه‌سازی و گزارش وضعیت
    print("Initializing simulation parameters...")
    timeout_duration = t_d
    increse_window_size_duration = i_w_s_d
    wait_time = w_t
    rtt = r  # مقدار RTT پیش‌فرض
    window_size = w_s  # اندازه پنجره اولیه
    time.sleep(0.1)  # شبیه‌سازی زمان مقداردهی اولیه پارامترهای شبیه‌سازی
    return timeout_duration, increse_window_size_duration, wait_time, rtt, window_size

def packet_loss_rate():
    # تولید نرخ اتلاف بسته‌ها به صورت درصدی
    return random.random() < 0.1  # برای مثال، نرخ اتلاف ۱۰٪ است

def main():
    global increse_window_size_duration 
    global timeout_duration
    global wait_time
    global rtt
    global window_size  # تعریف متغیر گلوبال برای اندازه پنجره
    timeout_duration, increse_window_size_duration, wait_time, rtt, window_size = initialize_simulation_parameters(0.1, 0.2, 0.3, 5000, 10)
    while True:
        packet = random_packet(rtt)  # تولید یک پکت تصادفی
        if packet_loss_rate():
            # اگر یک بسته از بین برود، فرآیند ارسال و دریافت بسته مجدداً آغاز شود
            print("Packet loss! Resending packet...")
            send_packet(packet)
            wait_for_ack(wait_time)
            receive_ack(increse_window_size_duration)
        elif is_congested():
            # وقوع ازدحام و گزارش وضعیت
            print("Congestion occurred! Adjusting parameters...")
            window_size = tcp_tahoe_congestion_control(window_size)  # اعمال الگوریتم TCP Tahoe
        else:
            # ارسال پکت و دریافت تأییدیه
            send_packet(packet)
            wait_for_ack(wait_time)
            receive_ack(increse_window_size_duration)
        # اجرای timeout برای مدیریت اتلاف پکت
        timeout_for_packet_loss(timeout_duration)

if __name__ == "__main__":
    main()
