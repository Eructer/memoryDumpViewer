import os
from pathlib import Path

class Cache:
    def __init__(self):
        pass

    def clean_cache(self, cache_dir: str) -> bool:
        try:
            for file in os.listdir(cache_dir):
                file_path = os.path.join(cache_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return True
        except Exception as e:
            return False

    def is_cache_valid(self, cache_path: Path, chumk_num: int,chunk_size: int, source_file: str) -> bool:
        if not cache_path.exists():
            return False
        expected_offset = chumk_num * chunk_size
        file_size = os.path.getsize (source_file)

        expected_cache_size = min(chunk_size, file_size - expected_offset)
        actual_cache_size = cache_path.stat().st_size
        
        return actual_cache_size == expected_cache_size

    def ensure_chunk_cached(self, chunk_num: int, chunk_size:int, source_file: str, get_chunk_path) -> Path:
        cache_path = get_chunk_path(chunk_num)

        if not self.is_cache_valid(cache_path, chunk_num, chunk_size,source_file):
            with open(source_file, 'rb') as f:
                offset = chunk_num * chunk_size
                size = min(chunk_size, os.path.getsize(source_file) - offset)
                f.seek(offset)
                chunk_data = f.read(size)
            with open(cache_path.with_suffix('.tmp'), 'wb') as out:
                out.write(chunk_data)
            os.replace(cache_path.with_suffix('.tmp'), cache_path)
        return cache_path