
import os

files = os.listdir(os.path.join('./', 'output', 'p_dqn_train', '000070'))  # a2c 모델들 저장한 루트
file_h5 = [file for file in files if file.endswith(".h5")]

print(files)
print(file_h5)