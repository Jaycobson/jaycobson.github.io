# import dash
# from dash import dcc, html, Input, Output, dash_table, State
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# import numpy as np
# import base64
# import io
# from datetime import datetime

# # Initialize the Dash app
# app = dash.Dash(__name__)
# app.title = "Dynamic Data Dashboard"

# # Global variable to store uploaded data
# uploaded_data = None

# def parse_contents(contents, filename):
#     """Parse uploaded file contents"""
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
    
#     try:
#         if 'csv' in filename:
#             df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
#         elif 'xls' in filename:
#             df = pd.read_excel(io.BytesIO(decoded))
#         else:
#             return None, "Unsupported file format. Please upload CSV or Excel files."
        
#         return df, f"Successfully loaded {filename} with {len(df)} rows and {len(df.columns)} columns."
#     except Exception as e:
#         return None, f"Error processing file: {str(e)}"

# def detect_column_types(df):
#     """Automatically detect column types"""
#     numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
#     categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
#     # Try to detect date columns
#     date_cols = []
#     for col in categorical_cols:
#         try:
#             pd.to_datetime(df[col].dropna().head(100))
#             date_cols.append(col)
#         except:
#             continue
    
#     # Remove detected date columns from categorical
#     categorical_cols = [col for col in categorical_cols if col not in date_cols]
    
#     return numeric_cols, categorical_cols, date_cols

# def generate_automatic_charts(df):
#     """Generate charts automatically based on data structure"""
#     numeric_cols, categorical_cols, date_cols = detect_column_types(df)
#     charts = []
    
#     # 1. Summary statistics table
#     if numeric_cols:
#         summary_stats = df[numeric_cols].describe().round(2)
#         charts.append({
#             'type': 'table',
#             'title': 'Summary Statistics',
#             'data': summary_stats.reset_index().to_dict('records'),
#             'columns': [{'name': 'Statistic', 'id': 'index'}] + 
#                       [{'name': col, 'id': col, 'type': 'numeric'} for col in numeric_cols]
#         })
    
#     # 2. Correlation heatmap (if multiple numeric columns)
#     if len(numeric_cols) > 1:
#         corr_matrix = df[numeric_cols].corr()
#         charts.append({
#             'type': 'heatmap',
#             'title': 'Correlation Matrix',
#             'data': corr_matrix
#         })
    
#     # 3. Distribution plots for numeric columns
#     for col in numeric_cols[:4]:  # Limit to first 4 numeric columns
#         charts.append({
#             'type': 'histogram',
#             'title': f'Distribution of {col}',
#             'data': df[col].dropna(),
#             'column': col
#         })
    
#     # 4. Bar charts for categorical columns
#     for cat_col in categorical_cols[:3]:  # Limit to first 3 categorical columns
#         value_counts = df[cat_col].value_counts().head(10)
#         if len(value_counts) > 1:
#             charts.append({
#                 'type': 'bar',
#                 'title': f'Top 10 {cat_col}',
#                 'data': value_counts,
#                 'column': cat_col
#             })
    
#     # 5. Time series plots (if date columns exist)
#     if date_cols and numeric_cols:
#         date_col = date_cols[0]
#         numeric_col = numeric_cols[0]
#         try:
#             df_time = df[[date_col, numeric_col]].copy()
#             df_time[date_col] = pd.to_datetime(df_time[date_col])
#             df_time = df_time.sort_values(date_col)
#             charts.append({
#                 'type': 'timeseries',
#                 'title': f'{numeric_col} Over Time',
#                 'data': df_time,
#                 'date_col': date_col,
#                 'value_col': numeric_col
#             })
#         except:
#             pass
    
#     # 6. Scatter plots (if multiple numeric columns)
#     if len(numeric_cols) >= 2:
#         charts.append({
#             'type': 'scatter',
#             'title': f'{numeric_cols[0]} vs {numeric_cols[1]}',
#             'data': df[[numeric_cols[0], numeric_cols[1]]].dropna(),
#             'x_col': numeric_cols[0],
#             'y_col': numeric_cols[1],
#             'color_col': categorical_cols[0] if categorical_cols else None
#         })
    
#     return charts

# def create_chart(chart_info):
#     """Create plotly figure based on chart info"""
#     if chart_info['type'] == 'histogram':
#         fig = px.histogram(
#             x=chart_info['data'],
#             nbins=30,
#             title=chart_info['title'],
#             labels={'x': chart_info['column'], 'y': 'Count'}
#         )
    
#     elif chart_info['type'] == 'bar':
#         fig = px.bar(
#             x=chart_info['data'].index,
#             y=chart_info['data'].values,
#             title=chart_info['title'],
#             labels={'x': chart_info['column'], 'y': 'Count'}
#         )
    
#     elif chart_info['type'] == 'heatmap':
#         fig = px.imshow(
#             chart_info['data'],
#             text_auto=True,
#             aspect="auto",
#             title=chart_info['title'],
#             color_continuous_scale='RdBu'
#         )
    
#     elif chart_info['type'] == 'timeseries':
#         fig = px.line(
#             chart_info['data'],
#             x=chart_info['date_col'],
#             y=chart_info['value_col'],
#             title=chart_info['title']
#         )
    
#     elif chart_info['type'] == 'scatter':
#         fig = px.scatter(
#             chart_info['data'],
#             x=chart_info['x_col'],
#             y=chart_info['y_col'],
#             color=chart_info['color_col'],
#             title=chart_info['title']
#         )
    
#     else:
#         return go.Figure()
    
#     fig.update_layout(template="plotly_white")
#     return fig

# # App Layout
# app.layout = html.Div([
#     # Header
#     html.Div([
#         html.H1("Dynamic Data Dashboard", 
#                 style={'textAlign': 'center', 'color': '#1f2937', 'marginBottom': '10px'}),
#         html.P("Upload any CSV or Excel file to automatically generate interactive visualizations",
#                style={'textAlign': 'center', 'color': '#6b7280', 'fontSize': '16px'})
#     ], style={'padding': '20px', 'backgroundColor': '#f9fafb'}),
    
#     # File upload section
#     html.Div([
#         html.Div([
#             html.H3("📁 Upload Your Data", style={'color': '#374151', 'marginBottom': '20px'}),
#             dcc.Upload(
#                 id='upload-data',
#                 children=html.Div([
#                     html.I(className="fas fa-cloud-upload-alt", 
#                           style={'fontSize': '48px', 'color': '#3b82f6', 'marginBottom': '10px'}),
#                     html.Br(),
#                     'Drag and Drop or ',
#                     html.A('Select Files', style={'color': '#3b82f6', 'fontWeight': 'bold'}),
#                     html.Br(),
#                     html.Small('Supports CSV and Excel files', style={'color': '#6b7280'})
#                 ]),
#                 style={
#                     'width': '100%', 'height': '120px', 'lineHeight': '60px',
#                     'borderWidth': '2px', 'borderStyle': 'dashed',
#                     'borderRadius': '10px', 'textAlign': 'center', 'margin': '10px',
#                     'borderColor': '#3b82f6', 'backgroundColor': '#eff6ff'
#                 },
#                 multiple=False
#             ),
#             html.Div(id='upload-status', style={'marginTop': '10px'})
#         ], style={'textAlign': 'center'})
#     ], style={'margin': '20px', 'padding': '30px', 'backgroundColor': 'white', 
#               'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    
#     # Data preview section
#     html.Div(id='data-preview', style={'margin': '20px'}),
    
#     # Dashboard section
#     html.Div(id='dashboard-content', style={'margin': '20px'})
    
# ], style={'backgroundColor': '#f3f4f6', 'minHeight': '100vh'})

# # Callbacks
# @app.callback(
#     [Output('upload-status', 'children'),
#      Output('data-preview', 'children'),
#      Output('dashboard-content', 'children')],
#     [Input('upload-data', 'contents')],
#     [State('upload-data', 'filename')]
# )
# def update_output(contents, filename):
#     global uploaded_data
    
#     if contents is None:
#         return (
#             html.Div("No file uploaded yet.", style={'color': '#6b7280'}),
#             html.Div(),
#             html.Div()
#         )
    
#     # Parse the uploaded file
#     df, message = parse_contents(contents, filename)
    
#     if df is None:
#         return (
#             html.Div(message, style={'color': '#dc2626', 'fontWeight': 'bold'}),
#             html.Div(),
#             html.Div()
#         )
    
#     uploaded_data = df
    
#     # Create status message
#     status = html.Div([
#         html.P(message, style={'color': '#059669', 'fontWeight': 'bold'}),
#         html.P(f"Columns: {', '.join(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}")
#     ])
    
#     # Create data preview
#     preview = html.Div([
#         html.H4("📊 Data Preview", style={'color': '#374151', 'marginBottom': '20px'}),
#         html.Div([
#             html.Div([
#                 html.H5(f"{len(df)}", style={'color': '#059669', 'margin': '0', 'fontSize': '24px'}),
#                 html.P("Rows", style={'margin': '0', 'color': '#6b7280'})
#             ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#ecfdf5', 
#                      'borderRadius': '8px', 'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
#             html.Div([
#                 html.H5(f"{len(df.columns)}", style={'color': '#2563eb', 'margin': '0', 'fontSize': '24px'}),
#                 html.P("Columns", style={'margin': '0', 'color': '#6b7280'})
#             ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#eff6ff', 
#                      'borderRadius': '8px', 'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
#             html.Div([
#                 html.H5(f"{df.select_dtypes(include=[np.number]).shape[1]}", 
#                         style={'color': '#7c3aed', 'margin': '0', 'fontSize': '24px'}),
#                 html.P("Numeric Cols", style={'margin': '0', 'color': '#6b7280'})
#             ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#f5f3ff', 
#                      'borderRadius': '8px', 'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
#             html.Div([
#                 html.H5(f"{df.isnull().sum().sum()}", 
#                         style={'color': '#dc2626', 'margin': '0', 'fontSize': '24px'}),
#                 html.P("Missing Values", style={'margin': '0', 'color': '#6b7280'})
#             ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#fef2f2', 
#                      'borderRadius': '8px', 'width': '23%', 'display': 'inline-block', 'margin': '1%'})
#         ]),
        
#         html.H5("First 10 Rows:", style={'marginTop': '20px', 'color': '#374151'}),
#         dash_table.DataTable(
#             data=df.head(10).to_dict('records'),
#             columns=[{'name': i, 'id': i} for i in df.columns],
#             style_cell={'textAlign': 'left', 'padding': '10px'},
#             style_header={'backgroundColor': '#374151', 'color': 'white', 'fontWeight': 'bold'},
#             style_data_conditional=[
#                 {'if': {'row_index': 'odd'}, 'backgroundColor': '#f9fafb'}
#             ],
#             page_size=10
#         )
#     ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px',
#               'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    
#     # Generate automatic dashboard
#     charts = generate_automatic_charts(df)
#     dashboard_elements = []
    
#     dashboard_elements.append(
#         html.H3("🎯 Automatic Data Analysis", 
#                 style={'color': '#374151', 'textAlign': 'center', 'marginBottom': '30px'})
#     )
    
#     # Create chart elements
#     chart_row = []
#     for i, chart_info in enumerate(charts):
#         if chart_info['type'] == 'table':
#             dashboard_elements.append(
#                 html.Div([
#                     html.H5(chart_info['title'], style={'textAlign': 'center', 'color': '#374151'}),
#                     dash_table.DataTable(
#                         data=chart_info['data'],
#                         columns=chart_info['columns'],
#                         style_cell={'textAlign': 'center'},
#                         style_header={'backgroundColor': '#374151', 'color': 'white'}
#                     )
#                 ], style={'backgroundColor': 'white', 'borderRadius': '8px', 'padding': '20px',
#                          'margin': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
#             )
#         else:
#             fig = create_chart(chart_info)
#             chart_element = html.Div([
#                 dcc.Graph(figure=fig)
#             ], style={'width': '50%' if i % 2 == 0 else '50%', 'display': 'inline-block',
#                      'backgroundColor': 'white', 'borderRadius': '8px', 'padding': '10px',
#                      'margin': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
            
#             chart_row.append(chart_element)
            
#             # Add row every 2 charts
#             if len(chart_row) == 2:
#                 dashboard_elements.append(html.Div(chart_row))
#                 chart_row = []
    
#     # Add remaining charts
#     if chart_row:
#         dashboard_elements.append(html.Div(chart_row))
    
#     dashboard = html.Div(dashboard_elements)
    
#     return status, preview, dashboard

# if __name__ == '__main__':
#     app.run_server()