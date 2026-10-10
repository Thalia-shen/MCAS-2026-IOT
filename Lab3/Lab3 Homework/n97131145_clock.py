"""Lab3 作業 2：做出中間冒號會一秒閃一下的時鐘"""

import time

try:
    import tm1637
except ImportError:
    tm1637 = None


# tm1637 函式庫使用 BCM GPIO 編號。
# BCM 23 是實體腳位 16；BCM 24 是實體腳位 18。
CLK_PIN = 23
DIO_PIN = 24


def next_colon_state(current_state):
    """把冒號狀態由亮變暗，或由暗變亮。"""
    return not current_state


def clock_values(local_time):
    """從系統時間取出小時與分鐘。"""
    return local_time.tm_hour, local_time.tm_min


def main():
    if tm1637 is None:
        raise RuntimeError(
            "找不到 tm1637.py。請把這個程式放進同資料夾後再執行。"
        )

    display = tm1637.TM1637(clk=CLK_PIN, dio=DIO_PIN)
    display.brightness(1)
    show_colon = False

    print("時鐘已啟動，按 Ctrl+C 可停止程式。")

    try:
        while True:
            now = time.localtime()
            hour, minute = clock_values(now)
            show_colon = next_colon_state(show_colon)

            # 第三個參數控制中間冒號是否亮起。
            display.numbers(hour, minute, show_colon)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n時鐘已停止")
    finally:
        # 關閉四位七段顯示器上的所有燈段。
        display.write([0, 0, 0, 0])


if __name__ == "__main__":
    main()
