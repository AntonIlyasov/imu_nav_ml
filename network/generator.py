import json
import numpy as np
import create_dataset

file_type = {'json': 1, 'csv': 2}

class DatasetGenerator:
    def __init__(self, path, type_of_file):

        self.type_of_file = type_of_file

        self.dataset = {"x":[], "y":[]}
        self.x_train, self.y_train, self.x_test, self.y_test = [],[],[],[]
        self.threshold = 0.8
        
        if type_of_file == file_type['json']:
            self.data = self.read_serial_log(path)      # json
        elif type_of_file == file_type['csv']:
            pass

    def read_serial_log(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        return data

    def generate_dataset(self, net_hparams, colum_names):
        if self.type_of_file == file_type['json']:
            j = 0
            past = [self.data[0]["roll"], self.data[0]["pitch"], self.data[0]["heading"]]
            print("len(self.data): ", len(self.data))
            for i, item in enumerate(self.data):
                try:
                    data = list(map(float, item["value"].split("\t")[0:11:1]))
                    data[0] = data[0] / 100000
                    data[1] = data[1]/10
                    self.dataset["x"].append(data) # 11 features
                    self.dataset["y"].append([(item["pitch"]+np.pi/2)/np.pi,(item["roll"]+np.pi/2)/np.pi, (item["heading"]+np.pi/2)/np.pi])
                    past = [item["pitch"], item["roll"], item["heading"]]
                except ValueError:
                    continue
                j+=1
        elif self.type_of_file == file_type['csv']:
            self.x_train, self.y_train, self.x_test, self.y_test = create_dataset(net_hparams, colum_names)



    def return_set(self):

        if self.type_of_file == file_type['csv']:
            return np.array(self.x_train), np.array(self.y_train), np.array(self.x_test), np.array(self.y_test)

        else:
            print("type(self.dataset[\"x\"]): ", type(self.dataset["x"]))
            position = int(len(self.dataset["x"]) * self.threshold)
            return np.array(self.dataset["x"][0:position:1]), np.array(self.dataset["y"][0:position:1]), np.array(self.dataset["x"][position::1]), np.array(self.dataset["y"][position::1])


if __name__ == "__main__":
    gen = DatasetGenerator('serial_log.json')
    gen.generate_dataset()
    x_train, y_train, x_test, y_test = gen.return_set()