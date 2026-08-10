import os
from parser import Parser
from reader import Reader

path = "src/test/output.lime.compressed"
cache_dir = "src/main/cache"

file_size = os.path.getsize(path)

print(f"File size : {file_size} Bits")

print(f"Suggested chunk size : {8000000000} (1GB)")

chunk_size = 0

try:
    chunk_size = int(input("Input a chunk size: "))
    print(f"Using size : {chunk_size}")
except ValueError as e:
    print("Defaulting to : 8192 KB")
    chunk_size = 8192

parser = Parser(chunk_size, cache_dir)



passes = file_size // chunk_size 

print(f"Will run {passes} times")

proceed = input("Proceed (y/n) : ")

if proceed == "y":
    for i in range(1, passes, 1):
        parser.read_chunk(i, path)

read_path = "src/main/cache/000001.dat"
reader = Reader()
reader.print_file(read_path)