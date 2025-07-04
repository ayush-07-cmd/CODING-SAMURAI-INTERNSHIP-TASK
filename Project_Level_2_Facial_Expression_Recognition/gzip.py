import h5py
import numpy as np

# Example data to store in the dataset
your_data = np.random.rand(100, 100)  # Replace with your actual data
f = h5py.File(r'c:\Users\ayush\OneDrive\Desktop\Coding Samurai\Facial_Expression\gzip.py" "c:\Users\ayush\OneDrive\Desktop\Coding Samurai\Facial_Expression\h5py_gzip_example.py"
', 'w')
dset = f.create_dataset('data', data=your_data, compression="gzip", compression_opts=4)
f.close()