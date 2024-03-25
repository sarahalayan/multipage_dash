
import dash
from dash import dcc,html, callback
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import date
import pandas as pd
data = pd.read_csv(r'C:\Users\USER\Downloads\dash\2023_data.csv')

G=['Incomer G3','Incomer G4','Incomer 1 G2','Incomer 5 G1','Incomer 2 G5']
PV=['PV Gen','PV EDL']
EDL=['EDLTF-1','EDLTF-2','EDLTF-3']
generator_names = G + PV + EDL
all_column_names = data.columns
receiver_options=[name for name in all_column_names if name not in generator_names and name !='Date/time' ]



dash.register_page(__name__, path='/Consumption')
layout = html.Div([
        html.Div([
            html.Span("Receivers",style={'font-weight': 'bold', 'font-size': '2rem', 'text-align':'center','margin-left': '10%'})
        ]),
        html.Div([
            html.Span("Select receiver: ", style={'font-weight': 'bold', 'color': '#333', 'margin-bottom': '40px'}),
            dcc.Dropdown(
                id='y_axis_dropdown',
                options=[{'label': option, 'value': option} for option in receiver_options],
                value=receiver_options[0],
                multi=False
            ),
        ],
            style={'margin-bottom': 20, 'width': '50%', 'margin-left': '10%'}
        ),
        html.Div(
            dcc.Graph(id='the_graph'),
            style={'width': '80%', 'margin': 'auto', 'margin-top': 20}
        ),
        html.Div(
            [
                html.Span("Select date range: ", style={'font-weight': 'bold', 'color': '#333', 'margin-bottom': 40}),
                dcc.DatePickerRange(
                    id='date-picker-range1',
                    min_date_allowed=data['Date/time'].min(),
                    max_date_allowed=data['Date/time'].max(),
                    initial_visible_month=data['Date/time'].min()
                )
            ],
            style={'margin-top': 20, 'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}
        )  
], style={'background-color': '#f5f5f5', 'font-family': 'sans-serif'})



@callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='y_axis_dropdown', component_property='value'),
     Input('date-picker-range1', 'start_date'),
     Input('date-picker-range1', 'end_date')]
)
def update_graph(y_axis_dropdown,start_date, end_date):
    if start_date is not None and end_date is not None:
        filtered_data = data[
      (pd.to_datetime(data['Date/time']) >= start_date) &  
      (pd.to_datetime(data['Date/time']) <= end_date)
    ]
    else:
        filtered_data=data
    figure = px.line(
        filtered_data,
        x='Date/time',
        y=y_axis_dropdown  
    )
    return figure



