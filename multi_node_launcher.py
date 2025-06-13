import multiprocessing
import os

NODE_COUNT = 100

def launch_node(i):
    device_name = f"Device_{i+1}"
    os.system(f"python main_multi.py {device_name}")

if __name__ == "__main__":
    processes = []
    for i in range(NODE_COUNT):
        p = multiprocessing.Process(target=launch_node, args=(i,))
        p.start()
        processes.append(p)

    # 可选：等待所有进程结束
    for p in processes:
        p.join()
