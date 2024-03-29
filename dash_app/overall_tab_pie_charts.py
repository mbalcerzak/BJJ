import dash_core_components as dcc
import pandas as pd
import json
import plotly.express as px


def get_titles_dict(colname):
    with open(f'Dictionaries/colname_to_question.json', 'r') as f:
        file = json.load(f)

    return file[colname]


def get_pie_chart(file, colname):
    title = get_titles_dict(colname)

    df = pd.DataFrame(file[colname].items(), columns=['Label', 'Count'])
    df = df.sort_values(by=['Label'])

    fig = px.pie(df, values='Count', names='Label', title=title)

    return fig


def pie_charts_overall(data_all):
    return [
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
                        dcc.Graph(id='how_old_when_started_all',
                                  figure=get_pie_chart(data_all, 'current_age'),
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