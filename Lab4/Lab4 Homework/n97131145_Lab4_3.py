import serial
import time
import tm1637

# 設定四位數七段顯示器
display = tm1637.TM1637(clk=23, dio=24)
display.brightness(2)

# 設定 UART 連接埠與參數（預設使用 /dev/serial0）
ser = serial.Serial(
    port='/dev/serial0',      # 對應 GPIO14（TX）和 GPIO15（RX）
    baudrate=9600,            # 傳輸速率
    timeout=1                 # 讀取逾時設定（秒）
)

# 傳送資料
def send_data(data):
    if ser.is_open:
        ser.write(data.encode('utf-8'))
        print(f"已傳送：{data}")

# 接收資料
def receive_data():
    if ser.is_open:
        incoming = ser.readline().decode('utf-8').strip()

        if incoming:
            print(f"收到資料：{incoming}")

        return incoming

# 主程式
try:
    print("學號：n97131145")

    while True:
        send_data("1234\n")
        time.sleep(1)

        incoming = receive_data()

        if incoming:
            display.show(incoming)

        time.sleep(1)

except KeyboardInterrupt:
    print("程式中斷")

finally:
    # 清除七段顯示器畫面
    display.show("    ")

    if ser.is_open:
        ser.close()
        print("串列埠已關閉")