import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import base64
from plotly import graph_objects as go
import io
from plotly.subplots import make_subplots

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
    html.Div(id='graph-table-container', children=[]),
])

# Callback to update the layout with graphs and tables
@app.callback(
    Output('graph-table-container', 'children'),
    [Input('upload-data', 'contents')]
)
def update_layout(contents):
    if contents:
        # Extracting the data from the uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        file_path = io.StringIO(decoded.decode('utf-8'))

        data = {'time': [], 'size': [], 'address': [], 'source': [], 'line': [], 'thread_name': []}

        for line in file_path:
            parts = line.strip().split(',')

            # Check if there are enough parts in the line
            if len(parts) == 6:
                time = int(parts[0])
                size = int(parts[1])
                address = parts[2]
                source = parts[3]
                line = int(parts[4])
                thread_name = parts[5]

                data['time'].append(time)
                data['size'].append(size)
                data['address'].append(address)
                data['source'].append(source)
                data['line'].append(line)
                data['thread_name'].append(thread_name)
            else:
                print(f"Ignored line: {line.strip()} - Wrong format")

        df = pd.DataFrame(data)

        # Create subplots with shared x-axis
        graphs_and_tables = []
        for thread in df['thread_name'].unique():
            thread_data = df[df['thread_name'] == thread]

            # Create a graph for each thread
            fig = make_subplots(rows=1, cols=1)
            hovertext = [f"src:{source}<br>line:{line}" for source, line in zip(thread_data['source'], thread_data['line'])]
            fig.add_trace(
                go.Scatter(
                    x=thread_data['time'],
                    y=thread_data['size'].cumsum(),
                    mode='markers+lines',
                    name=thread,
                    hovertext=hovertext,
                    hoverinfo='text'  # Show hover text
                )
            )
            fig.update_layout(
                title_text=f"Thread: {thread}",
                xaxis_title="Time",
                yaxis_title="Cumulative Unreleased Memory Usage",
                margin=dict(l=50, r=50, b=50, t=50),  # Adjust margin for better layout
                title_x=0.5,  # Center the title horizontally
                title_y=0.9,  # Adjust the vertical position of the title
            )

            # Create data for the table
            table_data = thread_data.to_dict('records')

            # Create a table for each thread
            table = dash_table.DataTable(
                id={'type': 'table', 'index': thread},
                data=table_data,
                style_table={'minHeight': '100px', 'maxHeight': '500px', 'overflowY': 'auto', 'marginBottom': 100},
                fixed_rows={'headers': True, 'data': 0},
                selected_rows=[],
                style_cell={'textAlign': 'left', 'minWidth': '50px', 'maxWidth': '300px', 'whiteSpace': 'normal'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            )

            # Create a single div for each thread containing both the graph and table
            thread_div = html.Div([
                html.Div(dcc.Graph(figure=fig), style={'width': '70%'}),
                html.Div(table, style={'width': '30%'})
            ], style={'display': 'flex', 'flexDirection': 'row'})

            graphs_and_tables.append(thread_div)

        return graphs_and_tables

    # If no contents, return an empty list
    return []


# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
