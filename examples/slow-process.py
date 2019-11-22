import time

try:
    print('slow process starting')
    time.sleep(20)
finally:
    print('slow process end')
