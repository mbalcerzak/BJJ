import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Output, Input
import json

from dash_app.dash_header import app_header
from dash_app.overall_tab_pie_charts import pie_charts_overall
from dash_app.utils import get_list, get_genders, get_load_json_data_all
from src.data_processing import get_belt_colours


belts = get_list("belts")
genders = get_genders()
belt_colours = get_belt_colours()

data_all = get_load_json_data_all()

path_bjj_image_intro = 'jonathan-borba-Yf1SegAI84o-unsplash.jpg'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    app_header(),
    dcc.Tabs(id='tabs-example', value='tab-description', children=[
        dcc.Tab(label='Intro', value='tab-description'),
        dcc.Tab(label='See all answers', value='tab-overall'),
        dcc.Tab(label='Select a group', value='tab-grouped'),
    ]),
    html.Div(id='tabs-example-content')
])


@app.callback(
    Output('pie-chart-gender-belt', 'figure'),
    [Input('belt_dropdown', "value"),
     Input('gender_dropdown', "value")])
def update_figure(belt, gender):
    with open(f'Data/gender_belt/{gender}_{belt_colours[belt]}.json', 'r') as f:
        file = json.load(f)
        training_yrs = file["training_years"]

    df = pd.DataFrame(training_yrs.items(), columns=['Label', 'Count'])
    df = df.sort_values(by=['Label'])

    fig = px.pie(df, values='Count', names='Label')

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
                               'font-weight': 'bold',
                               'padding-top': '25px',
                               'padding-bottom': '25px'},
                        ),
            ]),
            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url(path_bjj_image_intro),
                             style={'height': '90%', 'width': '90%', 'padding-left': '50px'})
                ], className="six columns"),
                html.Div([
                    html.P('''Data comes from a survey about Brazilian jiu-jitsu (BJJ) created by Grumpy Grappler Blog. 
                    This app is visual a summary of 807 answers. You can find all the relevant links below''',
                           style={'textAlign': 'center',
                                  'color': '#1f3b4d',
                                  'fontSize': '22px',
                                  'padding-right': '50px'},
                           ),
                ], className="six columns"),
            ], className="row"),

        ],
        ),
    elif tab == 'tab-overall':
        return html.Div([
            html.Div([
                html.Div([
                    html.H5('Favourite things about BJJ',
                            style={'textAlign': 'center', 'marginBottom': 25, 'marginTop': 35, 'font-weight': 'bold'}),
                    html.Img(src=app.get_asset_url('wordcloud_favourite.png'),
                             style={'height': '95%', 'width': '95%', 'padding-left': '20px'})
                ], className="six columns"),
                html.Div([
                    html.H5('Why did you start training?',
                            style={'textAlign': 'center', 'marginBottom': 25, 'marginTop': 35, 'font-weight': 'bold'}),
                    html.Img(src=app.get_asset_url('wordcloud_reasons.png'),
                             style={'height': '95%', 'width': '95%', 'padding-right': '20px'})
                ], className="six columns"),
            ], className="row"),
            html.Div([
                html.H1('Overall statistics',
                        style={'textAlign': 'center',
                               'color': '#1f3b4d',
                               'fontSize': '35px',
                               'font-weight': 'bold',
                               'padding-top': '35px'},
                        ),
                html.Div(
                    children=pie_charts_overall(data_all)
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
                    value='black belt',
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
                dcc.Graph(id='pie-chart-gender-belt',
                          style={'padding': '25px'}),
            ),
        ]),


if __name__ == '__main__':
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=True)
