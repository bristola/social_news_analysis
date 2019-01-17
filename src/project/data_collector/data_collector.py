class Data_Collector():

    def __init__(self, out_file):
        self.output = out_file


    def write_to_file(self, data):
        with open(self.output, 'w+', encoding="utf-8") as f:
            f.write("\n".join(data))
