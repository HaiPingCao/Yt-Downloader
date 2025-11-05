import asyncio

from core.yt import *
from core.yt_options import Options
from utils.link import *
from utils.benchmark import *

from asyncio import Queue



async def worker(worker_id: int, url: str, queue: Queue, results: dict):
    """Worker lấy index từ queue và xử lý"""
    while True:
        index = None  # Khởi tạo index
        try:
            index = await queue.get()
            
            print(f"Worker {worker_id} đang xử lý index {index}...")
            
            # Lấy thông tin video
            options = Options(
                mode=2, 
                playlist=True, 
                debug=False, 
                playlist_items_index=f"{index}-{index}"
            )
            info = await extract_info(url, options)
            
            if info and len(info) > 0:
                title = info[0][0][0]
                duration = info[0][0][2]
                audio_url = info[0][0][3]
                results[index] = {
                    'title': title,
                    'duration': duration,
                    'audio_url': audio_url
                }
                print(f"✓ Worker {worker_id} hoàn thành index {index}: {title}")
            else:
                results[index] = None
                print(f"✗ Worker {worker_id} - Index {index}: Không có thông tin")
                
        except Exception as e:
            if index is not None:
                results[index] = None
                print(f"✗ Worker {worker_id} - Index {index}: Lỗi {e}")
            else:
                print(f"✗ Worker {worker_id}: Lỗi {e}")
        finally:
            if index is not None:
                queue.task_done()


async def main():
    url: str = "https://www.youtube.com/watch?v=oUHOyPvmLFU&list=RDoUHOyPvmLFU&start_radio=1"
    
    _link_type = link_type(url)
    start = 0
    
    try:
        end = get_playlist_count(url)
    except ValueError as ex:
        print(f"Không lấy được số lượng playlist: {ex}, mặc định 5")
        end = 5
    
    print(f"Link Type: {_link_type}, Tổng số items: {end}\n")
    
    # Tạo queue và thêm các index vào
    queue = Queue()
    for i in range(start, end):
        await queue.put(i + 1)
    
    # Dictionary để lưu kết quả
    results = {}
    
    # Tạo workers (số lượng worker tùy chỉnh)
    num_workers = 3
    workers = []
    for worker_id in range(1, num_workers + 1):
        task = asyncio.create_task(worker(worker_id, url, queue, results))
        workers.append(task)
    
    # Đợi queue xử lý xong
    await queue.join()
    
    # Hủy workers
    for w in workers:
        w.cancel()
    
    # In kết quả theo thứ tự
    print(f"\n{'='*60}")
    print("KẾT QUẢ CUỐI CÙNG:")
    print(f"{'='*60}\n")
    
    for index in sorted(results.keys()):
        if results[index]:
            print(f"{index}. {results[index]['title']} ({results[index]['duration']}s)")
        else:
            print(f"{index}. Không có dữ liệu")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())