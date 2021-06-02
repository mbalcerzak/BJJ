import dash_html_components as html


def app_header():
    return html.Div([
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
    )