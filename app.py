import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from dash.dependencies import Output, Input
import json


def get_list(name: str) -> dict:
    with open(f'Dictionaries/{name}.json', 'r') as f:
        file = json.load(f)

    sorted_list = sorted(file[name])

    options = []
    for key in sorted_list:
        options.append({'label': key, 'value': key})

    return options


def get_titles_dict(colname):
    with open(f'Dictionaries/colname_to_question.json', 'r') as f:
        file = json.load(f)

    return file[colname]


def get_load_json_data_all():
    with open(f'Data/bjj_overall.json', 'r') as f:
        file = json.load(f)

    return file


belts = get_list("belts")
genders = get_list("genders")
data_all = get_load_json_data_all()

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


def get_pie_chart(file, colname):
    title = get_titles_dict(colname)

    df = pd.DataFrame(file[colname].items(), columns=['Label', 'Count'])
    df = df.sort_values(by=['Label'])

    fig = px.pie(df, values='Count', names='Label', title=title)

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
                    html.Img(src=app.get_asset_url('../assets/wordcloud_favourite.png'),
                             style={'height': '100%', 'width': '100%'})
                ], className="six columns"),
                html.Div([
                    html.H5('Why did you start training?',
                            style={'textAlign': 'center', 'marginBottom': 25, 'marginTop': 35, 'font-weight': 'bold'}),
                    html.Img(src=app.get_asset_url('../assets/wordcloud_reasons.png'),
                             style={'height': '100%', 'width': '100%'})
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
                    children=[
                        dcc.Graph(id='current_belt_all',
                                  figure=get_pie_chart(data_all, 'current_belt'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='training_years_all',
                                  figure=get_pie_chart(data_all, 'training_years'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='white_blue_all',
                                  figure=get_pie_chart(data_all, 'white_blue'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='blue_purple_all',
                                  figure=get_pie_chart(data_all, 'blue_purple'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='purple_brown_all',
                                  figure=get_pie_chart(data_all, 'purple_brown'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='brown_black_all',
                                  figure=get_pie_chart(data_all, 'brown_black'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='training_per_week_all',
                                  figure=get_pie_chart(data_all, 'training_per_week'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='both_gi_nogi_all',
                                  figure=get_pie_chart(data_all, 'both_gi_nogi'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='gi_or_no_gi_all',
                                  figure=get_pie_chart(data_all, 'gi_or_no_gi'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='gym_self_defense_all',
                                  figure=get_pie_chart(data_all, 'gym_self_defense'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='training_time_all',
                                  figure=get_pie_chart(data_all, 'training_time'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='travel_all',
                                  figure=get_pie_chart(data_all, 'travel'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='background_ma_all',
                                  figure=get_pie_chart(data_all, 'background_ma'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='how_old_when_started_all',
                                  figure=get_pie_chart(data_all, 'how_old_when_started'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='instrutor_encourages_competition_all',
                                  figure=get_pie_chart(data_all, 'instrutor_encourages_competition'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='competed_all',
                                  figure=get_pie_chart(data_all, 'competed'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='medals_all',
                                  figure=get_pie_chart(data_all, 'medals'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='gym_curriculum_all',
                                  figure=get_pie_chart(data_all, 'gym_curriculum'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='currently_cross_train_all',
                                  figure=get_pie_chart(data_all, 'currently_cross_train'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='mobility_exercises_all',
                                  figure=get_pie_chart(data_all, 'mobility_exercises'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='yoga_all',
                                  figure=get_pie_chart(data_all, 'yoga'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='num_gis_all',
                                  figure=get_pie_chart(data_all, 'num_gis'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='num_rashguards_all',
                                  figure=get_pie_chart(data_all, 'num_rashguards'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='num_shorts_all',
                                  figure=get_pie_chart(data_all, 'num_shorts'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='bjj_apparel_all',
                                  figure=get_pie_chart(data_all, 'bjj_apparel'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='money_for_gear_all',
                                  figure=get_pie_chart(data_all, 'money_for_gear'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='membership_all',
                                  figure=get_pie_chart(data_all, 'membership'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='time_watching_bjj_all',
                                  figure=get_pie_chart(data_all, 'time_watching_bjj'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='education_all',
                                  figure=get_pie_chart(data_all, 'education'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='gender_all',
                                  figure=get_pie_chart(data_all, 'gender'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='income_all',
                                  figure=get_pie_chart(data_all, 'income'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='race_all',
                                  figure=get_pie_chart(data_all, 'race'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='do_watch_sport_bjj_all',
                                  figure=get_pie_chart(data_all, 'do_watch_sport_bjj'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='have_fav_athlete_all',
                                  figure=get_pie_chart(data_all, 'have_fav_athlete'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='leg_lock_friendly_all',
                                  figure=get_pie_chart(data_all, 'leg_lock_friendly'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='preferred_style_all',
                                  figure=get_pie_chart(data_all, 'preferred_style'),
                                  style={'padding': '5px'}),
                        dcc.Graph(id='choke_all',
                                  figure=get_pie_chart(data_all, 'choke'),
                                  style={'padding': '5px'}),
                    ]
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
