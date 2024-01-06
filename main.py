import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def select_file():
    file_path = filedialog.askopenfilename(title="Select a .txt file", filetypes=[("Text files", "*.txt")])
    if file_path:
        print(f"Selected file: {file_path}")
        return file_path
    return None

def show_heap(file_path):
    if file_path:
        # Assuming the .txt file contains lines with "x=10, y=10, comment=lodz"
        x_values = []
        y_values = []
        comments = []

        with open(file_path, 'r') as file:
            for line in file:
                # Extracting 'x', 'y', and 'comment' values from each line
                parts = line.strip().split(',')
                x = int(parts[0].split('=')[1])
                y = int(parts[1].split('=')[1])
                comment = parts[2].split('=')[1]
                x_values.append(x)
                y_values.append(y)
                comments.append(comment)

        # Plotting the data with annotations
        plt.scatter(x_values, y_values, label='Points')
        for i, comment in enumerate(comments):
            plt.annotate(comment, (x_values[i], y_values[i]), textcoords="offset points", xytext=(5,5), ha='center')

        plt.title('Scatter Plot with Comments')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.show()

# Create the main window
app = tk.Tk()
app.title("Select heap log")

# Create the "Select File" button
select_button = tk.Button(app, text="Select File", command=lambda: show_heap(select_file()))
select_button.pack(pady=10)

# Run the application
app.mainloop()
