import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Output, Input
import json
from skimage import io


def get_list(name: str) -> dict:
    with open(f'Dictionaries/{name}.json', 'r') as f:
        file = json.load(f)

    sorted_list = sorted(file[name])

    options = []
    for key in sorted_list:
        options.append({'label': key, 'value': key})

    return options


belts = get_list("belts")
genders = get_list("genders")

path_bjj_image_intro = '../assets/jonathan-borba-Yf1SegAI84o-unsplash.jpg'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div([
    html.Div([
        html.H1('Brasilian Jiu Jitsu survey results',
                style={'textAlign': 'center',
                       'color': '#FFFFFF',
                       'fontSize': '36px',
                       'padding-top': '0px'},
                ),

        html.P('By MAB', style={'textAlign': 'center',
                                'color': '#FFFFFF',
                                'fontSize': '24px'},
               ),
        html.P('''An interactive visualisation of a BJJ survey conducted online in 2017''',
               style={'textAlign': 'center',
                      'color': '#FFFFFF',
                      'fontSize': '16px'},
               ),
    ],
        style={'backgroundColor': '#1f3b4d',
               'height': '200px',
               'display': 'flex',
               'flexDirection': 'column',
               'justifyContent': 'center'},
    ),
    dcc.Tabs(id='tabs-example', value='tab-overall', children=[
        dcc.Tab(label='Intro', value='tab-description'),
        dcc.Tab(label='See all answers', value='tab-overall'),
        dcc.Tab(label='Select a group', value='tab-grouped'),
    ]),
    html.Div(id='tabs-example-content')
])


@app.callback(
    Output('pie-chart', 'figure'),
    [Input('belt_dropdown', "value"),
     Input('gender_dropdown', "value")])
def update_figure(belt, gender):
    with open(f'Data/bjj_overall.json', 'r') as f:
        file = json.load(f)
        training_yrs = file["training_years"]

    df = pd.DataFrame(training_yrs.items(), columns=['Years', 'Count'])
    df = df.sort_values(by=['Years'])

    fig = px.pie(df, values='Count', names='Years')

    return fig



@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-description':
        return html.Div([
            html.Div([
                html.H1('About the project',
                        style={'textAlign': 'center',
                               'color': '#1f3b4d',
                               'fontSize': '30px',
                               'padding-top': '15px'},
                        ),
            ]),
            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url(path_bjj_image_intro),
                             style={'height': '50%', 'width': '50%'})
                ], className="six columns"),
                html.Div([
                    html.P('''Data comes from a survey about Brazilian jiu-jitsu (BJJ) created by Grumpy Grappler Blog. 
                    The app is a summary of 807 answers. The free-text answers have been cleaned, you can check out
                     the methodology and my code on my GitHub''',
                       style={'textAlign': 'center',
                              'color': '#1f3b4d',
                              'fontSize': '16px'},
                       ),
                ], className="six columns"),
            ], className="row"),

        ],
        ),

    elif tab == 'tab-overall':
        return html.Div([
            html.Div([
                html.Div([
                    html.H4('Number of flats in each district', style={'textAlign': 'center'}),
                    dcc.Graph(id='pie_flats_per_location',
                              style={'padding': '25px'}),
                ], className="six columns"),
                html.Div([
                    html.H4('Size of flats (m2)', style={'textAlign': 'center'}),
                    dcc.Graph(id='pie_flats_per_area_cat',
                              style={'padding': '25px'}),
                ], className="six columns"),
            ], className="row"),
            html.Div([
                html.H1('Overall statistics',
                        style={'textAlign': 'center',
                               'color': '#1f3b4d',
                               'fontSize': '30px',
                               'padding-top': '15px'},
                        ),
            ]),

        ],
        ),
    elif tab == 'tab-grouped':
        return html.Div([
            html.H1('You can filter the data by belt colour, gender or both',
                    style={'textAlign': 'center',
                           'color': '#1f3b4d',
                           'fontSize': '30px',
                           'padding-top': '15px'},
                    ),
            html.Div([
                html.Label('Select a belt'),
                dcc.Dropdown(
                    id='belt_dropdown',
                    options=belts,
                    value='blue belt',
                    multi=False,
                    clearable=True,
                    searchable=True,
                    placeholder='Choose a belt colour...',
                ),
            ],
                style={'width': '25%',
                       'display': 'inline-block',
                       'padding-left': '150px',
                       'padding-top': '20px'}
            ),
            html.Div([
                html.Label('Select gender'),
                dcc.Dropdown(
                    id='gender_dropdown',
                    options=genders,
                    value='Male',
                    multi=False,
                    clearable=True,
                    searchable=True,
                    placeholder='Choose a gender...',
                ),
            ],
                style={'width': '25%',
                       'display': 'inline-block',
                       'padding-left': '150px',
                       'padding-top': '20px'}
            ),
            html.Div(
                dcc.Graph(id='pie-chart',
                          style={'padding': '25px'}),
            ),
        ]),


if __name__ == '__main__':
    app.run_server(debug=True)
