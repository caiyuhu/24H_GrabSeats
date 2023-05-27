import threading

from SHU24hAPI import SHU24hAPI

if __name__ == "__main__":
    api = SHU24hAPI()
    # 单线程登陆
    api.login()

    # 多线程执行grab grab内部每一个时间段中也涉及多线程，每个时间段对应一个线程 两层多线程
    threads = []
    for i in range(5):
        t = threading.Thread(target=api.grab)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
