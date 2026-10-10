"""Lab3 作業 1：同時用燈泡跟蜂鳴器用摩斯密碼打 "SOS" (3短 3長 3短)"""

import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None


# 使用 BOARD 編號，也就是樹莓派排針上的「實體腳位編號」。
LED_PIN = 11       # 實體腳位 11，對應 GPIO17
BUZZER_PIN = 13    # 實體腳位 13，對應 GPIO27

# 摩斯密碼的基本時間單位（秒）。
# 短訊號為 1 單位，長訊號為 3 單位。
UNIT = 0.2

SOS_PATTERN = "...---..."
MORSE_LETTERS = ("...", "---", "...")


def signal_duration(symbol):
    """依照摩斯符號回傳亮燈及發聲的時間。"""
    if symbol == ".":
        return UNIT
    if symbol == "-":
        return UNIT * 3
    raise ValueError("摩斯符號只能是 '.' 或 '-'")


def send_signal(pwm, symbol):
    """讓 LED 與蜂鳴器同步輸出一個短訊號或長訊號。"""
    duration = signal_duration(symbol)

    GPIO.output(LED_PIN, GPIO.HIGH)
    pwm.ChangeDutyCycle(50)
    time.sleep(duration)

    GPIO.output(LED_PIN, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

    # 同一個字母內，相鄰訊號之間間隔 1 單位。
    time.sleep(UNIT)


def send_sos(pwm):
    """依序輸出 S（3短）、O（3長）、S（3短）。"""
    for letter_index, letter in enumerate(MORSE_LETTERS):
        for symbol in letter:
            send_signal(pwm, symbol)

        # send_signal 已經停了 1 單位；再停 2 單位，
        # 讓不同字母之間的總間隔成為 3 單位。
        if letter_index < len(MORSE_LETTERS) - 1:
            time.sleep(UNIT * 2)


def main():
    if GPIO is None:
        raise RuntimeError("找不到 RPi.GPIO，請在樹莓派上執行這個程式。")

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)

    # 以 1000 Hz 控制蜂鳴器；占空比 0 表示先保持靜音。
    pwm = GPIO.PWM(BUZZER_PIN, 1000)
    pwm.start(0)

    try:
        print("開始輸出 SOS：3短、3長、3短")
        send_sos(pwm)
        print("SOS 輸出完成")
    finally:
        pwm.ChangeDutyCycle(0)
        pwm.stop()
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.cleanup()


if __name__ == "__main__":
    main()
