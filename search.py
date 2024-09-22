import concurrent.futures
from datetime import datetime
from pathlib import Path
from turtledemo.penrose import start

startTime = datetime.now()
print(f'startTime: {startTime}')


def search(path, pattern):
    root_path = Path(path)
    for path in root_path.rglob(pattern):
        yield path


def worker(path, pattern):
    return list(search(path, pattern))


root_directory = 'C:\\'
file_name = 'color1.py'

# 使用ThreadPoolExecutor来并发执行搜索任务
with concurrent.futures.ThreadPoolExecutor() as executor:
    # 假设我们将根目录分割成几个子目录进行搜索
    sub_dirs = [str(p) for p in Path(root_directory).iterdir() if p.is_dir()]
    futures = {executor.submit(worker, dir, file_name): dir for dir in sub_dirs}

    for future in concurrent.futures.as_completed(futures):
        dir = futures[future]
        try:
            results = future.result()
            for result in results:
                print(f'file_path: {result}, date: {datetime.now()}')
        except Exception as exc:
            print(f'{dir} generated an exception: {exc}')

print(f'FinishedTime: {datetime.now()}, Total time: {datetime.now() - startTime}')