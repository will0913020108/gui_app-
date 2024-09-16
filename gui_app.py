import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import tensorflow as tf
import os

# Load the model using TensorFlow
model_path = '/Users/williamhan/Desktop/mosquito pd'
model = tf.saved_model.load(model_path)

def predict_image(image_array):
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    infer = model.signatures['serving_default']
    predictions = infer(tf.constant(image_array, dtype=tf.float32))

    # Print the available keys in the predictions dictionary
    print("Available keys in predictions:", predictions.keys())
    
    # Use the correct key for accessing predictions
    prediction_array = list(predictions.values())[0].numpy().flatten()
    
    species_pred = "Male Aedes aegypti" if prediction_array[0] > prediction_array[1] else "Female Aedes aegypti"
    return species_pred

def predict_and_contrast_batch(file_paths):
    results_text.delete(1.0, tk.END)  # Clear previous results
    for file_path in file_paths:
        image = Image.open(file_path)
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0  # Normalize the image

        species_pred = predict_image(image_array)
        
        # Extract expected species from filename
        filename = os.path.basename(file_path)
        if 'AEGm' in filename:
            expected_species = "Male Aedes aegypti"
        elif 'AEGf' in filename:
            expected_species = "Female Aedes aegypti"
        else:
            expected_species = "Unknown"

        # Create a result string and highlight mismatches
        result = f"File: {filename}\nPrediction: {species_pred}\nExpected: {expected_species}\n"
        if species_pred != expected_species:
            result += "Mismatch: Result is highlighted in red!"
            result_color = 'red'
        else:
            result_color = 'black'

        # Add result to the text widget
        results_text.insert(tk.END, result + '\n' + '-'*50 + '\n')
        
        # Tag the mismatch lines
        if species_pred != expected_species:
            mismatch_start = 'end-2l'
            mismatch_end = 'end-1l'
            results_text.tag_add(filename, mismatch_start, mismatch_end)
            results_text.tag_config(filename, foreground=result_color)

def open_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if file_paths:
        predict_and_contrast_batch(file_paths)

# Create the main window
root = tk.Tk()
root.title("Mosquito Species Predictor")

# Create a button to open files
open_button = tk.Button(root, text="Open Image Files", command=open_files)
open_button.pack(pady=10)

# Create a text widget to display results
results_text = tk.Text(root, wrap=tk.WORD, height=20, width=80)
results_text.pack(padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
