class Reader:
    def __init__(self):
        pass

    def print_file(self, file_path:str) -> None:
        with open(file_path, "rb") as file:
            for line in file:
                temp = str(line).replace(r"\x"," ")
                print(temp)

    def read(self, file_path: str) -> list:
        content = []
        with open(file_path, "rb") as file:
            for line in file:
                temp = str(line).replace(r"\x"," ")
                content.append(temp)
        return content

    