import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

def select_file():
    file_path = filedialog.askopenfilename(title="Select a .txt file", filetypes=[("Text files", "*.txt")])
    if file_path:
        print(f"Selected file: {file_path}")
        return file_path
    return None

def show_heap(file_path):
    if file_path:
        # Assuming the .txt file contains lines with "size=10, y=10, comment=file,line, thread=Thread1"
        x_values = {}
        y_values = {}
        comments = {}

        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                
                # Check if there are enough parts in the line
                if len(parts) >= 4:
                    x = int(parts[0].split('=')[1])
                    y = int(parts[1].split('=')[1])
                    comment = parts[2].split('=')[1]
                    thread = parts[3].split('=')[1]

                    if thread not in x_values:
                        x_values[thread] = []
                        y_values[thread] = []
                        comments[thread] = []

                    x_values[thread].append(x)
                    if y_values[thread]:  # If y_values is not empty
                        y_values[thread].append(y + y_values[thread][-1])  # Add to the cumulative sum
                    else:
                        y_values[thread].append(y)  # Initial value
                    comments[thread].append(comment)
                else:
                    print(f"Ignored line: {line.strip()} - Not enough components")

        # Plotting the data with annotations for each thread
        for thread in x_values:
            plt.figure()  # Create a new figure for each thread
            plt.scatter(x_values[thread], y_values[thread], label=f'{thread}')
            for i, comment in enumerate(comments[thread]):
                plt.annotate(comment, (x_values[thread][i], y_values[thread][i]), textcoords="offset points", xytext=(5, 5), ha='center')

            plt.title(f'Unreleased Memory Over Time - {thread}')
            plt.xlabel('Time')
            plt.ylabel('Unreleased Memory Usage')
            plt.legend()
            plt.show(block=False)

# Create the main window
app = tk.Tk()
app.title("Select heap log")

# Create the "Select File" button
select_button = tk.Button(app, text="Select File", command=lambda: show_heap(select_file()))
select_button.pack(pady=10)

# Run the application
app.mainloop()
