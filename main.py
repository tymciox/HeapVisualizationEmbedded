import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import base64
from plotly import graph_objects as go
import io
from plotly.subplots import make_subplots

# ... (your existing imports)

# Create the main app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Unreleased Memory Over Time"),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Select File'),
        multiple=False
    ),
    html.Div([
        dcc.Graph(id='heap-graph'),
    ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'top'}),
    
    html.Div([
        dash_table.DataTable(id='heap-table'),
    ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}),
])

# Callback to update the graph and table based on the uploaded file
@app.callback(
    [Output('heap-graph', 'figure'),
     Output('heap-table', 'data')],
    [Input('upload-data', 'contents')]
)
def update_graph_and_table(contents):
    if contents:
        # Extracting the data from the uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        file_path = io.StringIO(decoded.decode('utf-8'))

        data = {'x': [], 'y': [], 'comment': [], 'thread': []}

        for line in file_path:
            parts = line.strip().split(',')

            # Check if there are enough parts in the line
            if len(parts) >= 4:
                x = int(parts[0].split('=')[1])
                y = int(parts[1].split('=')[1])
                comment = f"src:{parts[2].split('=')[1].split('/')[0]}<br>line:{parts[2].split('/')[1]}"  # Add "src:" and "line" to comments
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

        # Create data for the table
        table_data = df.to_dict('records')

        return fig, table_data

    # If no contents, return default values
    return go.Figure(), []

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
