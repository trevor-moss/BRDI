import h5py
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Listbox, MULTIPLE, Button, END, Scrollbar, Entry

# Function to plot selected datasets and columns
def plot_data():
    selected_datasets = [dataset_listbox.get(i) for i in dataset_listbox.curselection()]
    selected_columns = [(column_listbox.get(i)) for i in column_listbox.curselection()]

    if not selected_datasets or not selected_columns:
        print("Please select at least one dataset and one column to plot.")
        return
    
    with h5py.File(hdf5_filename, 'r') as hdf5_file:
        plt.figure(figsize=(10, 6))
        
        for dataset_name in selected_datasets:
            data = hdf5_file[dataset_name][:]
            
            for col in selected_columns:
                x_data = data['F1Time']
                y_data = data[col]
                plt.plot(x_data, y_data, label=f"{dataset_name} - Column {col}")
        

        plt.xlabel('Elapsed Time')
        plt.ylabel('Value')
        plt.title('Selected Datasets and Columns')
        plt.legend()
        plt.grid(True)
        plt.show()

# Function to update the dataset listbox based on the search query
def update_listbox(*args):
    search_query = search_var.get().lower()
    current_selection = [dataset_listbox.get(i) for i in dataset_listbox.curselection()]
    dataset_listbox.delete(0, END)
    
    # Always include selected datasets
    selected_filtered_datasets = sorted(current_selection)
    
    # Include only non-selected datasets that match the search query
    non_selected_filtered_datasets = sorted([dataset for dataset in datasets if search_query in dataset.lower() and dataset not in current_selection])
    
    # Add selected datasets to the top
    for dataset in selected_filtered_datasets:
        dataset_listbox.insert(END, dataset)
        dataset_listbox.selection_set(END)
    
    # Add non-selected datasets
    for dataset in non_selected_filtered_datasets:
        dataset_listbox.insert(END, dataset)

# Path to the HDF5 file
hdf5_filename = 'bioreactorData.h5'

# Open the HDF5 file and retrieve dataset names
with h5py.File(hdf5_filename, 'r') as hdf5_file:
    datasets = list(hdf5_file.keys())

# Create the main window
root = Tk()
root.title("HDF5 Data Plotter")

# Database search label
Label(root, text="Dataset Search").pack()

# Search bar
search_var = Entry(root)
search_var.pack()
search_var.bind('<KeyRelease>', update_listbox)

# Dataset listbox
Label(root, text="Select Datasets:").pack()
dataset_listbox = Listbox(root, selectmode=MULTIPLE, exportselection=0)
dataset_listbox.pack()
for dataset in datasets:
    dataset_listbox.insert(END, dataset)

# Column listbox
Label(root, text="Select Columns:").pack()
column_listbox = Listbox(root, selectmode=MULTIPLE, exportselection=0)
column_listbox.pack()

# Assuming all datasets have the same number of columns, we'll check the first dataset for the column count
with h5py.File(hdf5_filename, 'r') as hdf5_file:
    columns = hdf5_file[datasets[0]].dtype.names

for col in columns:
    column_listbox.insert(END, col)

# Plot button
plot_button = Button(root, text="Plot", command=plot_data)
plot_button.pack()

# Run the main loop
root.mainloop() 