import tkinter as tk
from tkinter import filedialog
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def select_file():
    file_path = filedialog.askopenfilename(title="Select a .txt file", filetypes=[("Text files", "*.txt")])
    if file_path:
        print(f"Selected file: {file_path}")
        return file_path
    return None

def show_heap(file_path):
    if file_path:
        # Assuming the .txt file contains lines with "size=10, y=10, comment=file/line, thread=Thread1"
        data = {'x': [], 'y': [], 'comment': [], 'thread': []}

        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                
                # Check if there are enough parts in the line
                if len(parts) >= 4:
                    x = int(parts[0].split('=')[1])
                    y = int(parts[1].split('=')[1])
                    comment = parts[2].split('=')[1]
                    thread = parts[3].split('=')[1]

                    data['x'].append(x)
                    data['y'].append(y)
                    data['comment'].append(comment)
                    data['thread'].append(thread)
                else:
                    print(f"Ignored line: {line.strip()} - Not enough components")

        df = pd.DataFrame(data)

        # Create subplots with shared x-axis
        fig = make_subplots(rows=len(df['thread'].unique()), cols=1, shared_xaxes=True, subplot_titles=list(df['thread'].unique()))

        for i, thread in enumerate(df['thread'].unique()):
            thread_data = df[df['thread'] == thread]
            fig.add_trace(
                go.Scatter(
                    x=thread_data['x'],
                    y=thread_data['y'].cumsum(),
                    mode='markers+lines',
                    name=thread,
                    hovertext=thread_data['comment'],  # Include comments as hover text
                    hoverinfo='text'  # Show hover text
                ),
                row=i+1, col=1
            )

        # Update layout
        fig.update_layout(
            title_text="Unreleased Memory Over Time",
            xaxis_title="Time",
            yaxis_title="Cumulative Unreleased Memory Usage"
        )

        # Show the plot
        fig.show()

# Create the main window
app = tk.Tk()
app.title("Select heap log")

# Create the "Select File" button
select_button = tk.Button(app, text="Select File", command=lambda: show_heap(select_file()))
select_button.pack(pady=10)

# Run the application
app.mainloop()
