import os


def generate_file(dir, filetype='txt'):
    for file in os.listdir(dir):
        if file.split('.')[-1] == filetype:
            yield InputData(os.path.join(dir, file))


class InputData:
    def __init__(self, path):
        self.path = path

    def read(self):
        return open(self.path).read()

    def readByLine(self):
        file = open(self.path)
        while True:
            data = file.readline()
            if not data:
                file.close()
                break
            yield data

    def readByBlock(self, block_size=1024):
        file = open(self.path)
        while True:
            data = file.read(block_size)
            if not data:
                file.close
                break
            yield data