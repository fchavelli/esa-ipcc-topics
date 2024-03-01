import pickle

ecvs_file_path = './data/cci/ecvs.pkl'
with open(ecvs_file_path, 'rb') as file:
    ecv_instances = pickle.load(file)

for ecv in ecv_instances:
    #ecv.display()
    print(ecv.name, ecv.project)