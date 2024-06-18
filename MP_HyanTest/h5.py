from keras.models import load_model
import h5py
import numpy as np

# Load the Keras model
model = load_model(r'C:\Users\hyanx\Documents\Thesis\Kaway-GUI\model\vocab_A.h5')

# Display the model summary
model.summary()

# Open the same file to read additional data if needed
with h5py.File(r'C:\Users\hyanx\Documents\Thesis\Kaway-GUI\model\vocab_A.h5', 'r') as file:
    # List all groups
    print("Keys: %s" % file.keys())
    
    # Example: Access a specific dataset if it exists
    if 'my_dataset' in file:
        data = file['my_dataset']
        data_array = np.array(data)
        print(data_array)
