import os
from pathlib import Path
from typing import BinaryIO
from fastapi import UploadFile
from cache import Cache


class Parser:
    def __init__(self, chunk_size: int, cache_dir: str):
        self.chunk_size = chunk_size
        self.cache_dir = Path(cache_dir)
        self.cache_handle = Cache()

    def read_chunk_from_bytes(self, chunk_num: int, source: UploadFile):
        cache_path = self.cache_handle.ensure_chunk_cached_from_upload(chunk_num, self.chunk_size, source, self._get_chunk_path)
        with open(cache_path, 'rb') as f:
            return f.read()

    def read_chunk(self, chunk_num: int, source_file: str):
        cache_path = self.cache_handle.ensure_chunk_cached(chunk_num, self.chunk_size, source_file, self._get_chunk_path)
        with open(cache_path, 'rb') as f:
            return f.read()

    def read_raw_bytes(self, source_file: str, offset: int, size: int) -> bytes:
        chunk_num = offset // self.chunk_size
        local_offset = offset % self.chunk_size
        chunk_size = min(self.chunk_size, os.path.getsize(source_file) - offset)

        cache_path = self.cache_handle.ensure_chunk_cached(chunk_num, self.chunk_size, source_file, self._get_chunk_path)
        with open(cache_path, 'rb') as f:
            f.seek(local_offset)
            return f.read(min(size, os.path.getsize(source_file) - offset))

    def _get_chunk_path(self, chunk_num: int) -> Path:
        self.cache_dir.mkdir(exist_ok=True)
        return self.cache_dir / f"{chunk_num:06d}.dat"

    