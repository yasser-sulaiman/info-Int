from dash import Dash
from dash import html, dcc, dash_table
import dash
import pandas as pd
import dash_bootstrap_components as dbc
# dash application
app = dash.Dash(__name__)

data = pd.read_csv("data/manual_integrated_data.csv")

app.layout = html.Div(
    children=[
        html.H1("EUROPEAN FOOTBALL LEAGUES"),
        # make the dropdowns in a div for styling
        html.Div(
            [
                # dropdown for Year
                # add title to the dropdown
                html.P(
                    [
                        "Select Year",
                        dcc.Dropdown(
                            id='Year',
                            options=sorted(data['Year'].unique()),
                            value=2015
                        ),
                    ]
                ),
 
                
                # dropdown for League
                # add title to the dropdown
                html.P(
                    [
                        "Select League",
                        dcc.Dropdown(
                            id='League',
                            options=sorted(data['League'].unique()),
                            value='Premier League'
                        ),
                    ]
                ),

                # dropdown for HomeTeam
                # add title to the dropdown
                html.P(
                    [
                        "Select HomeTeam",
                        dcc.Dropdown(
                            id='HomeTeam',
                            options=sorted(data['HomeTeam'].unique()),
                            value='Arsenal'
                        ),
                    ]
                ),
                # dropdown for AwayTeam
                # add title to the dropdown
                html.P(
                    [
                        "Select AwayTeam",
                        dcc.Dropdown(
                            id='AwayTeam',
                            options=sorted(data['AwayTeam'].unique()),
                            value='Chelsea'
                        ),
                    ]
                ),
            ],
            className='dropdown-container',
        ),

        # submit button
        html.Button(id='submit-button', n_clicks=0, children='Submit'),

        # most goals league
        html.Button(id='most-goals-league', n_clicks=0, children='Most Goals League'),

        # most goals team
        html.Button(id='most-goals-team', n_clicks=0, children='Most Goals Team'),

        # div for displaying the result
        html.H2("Results Most Goals League"),
        html.Div(id='results-league', style={'height': '25'}),

        # div for displaying the result
        html.H2("Results Most Goals Team"),
        html.Div(id='results-team', style={'height': '25'}),

        # div for displaying the result
        html.H2("Results"),
        html.Div(id='result', style={'overflow': 'scroll', 'height': '400px'})

    ]
)

# callback for the submit button, this callback will be triggered when the button is clicked
# it will take the values from the dropdowns and update the result div
@app.callback(
    dash.dependencies.Output('result', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('Year', 'value'),
     dash.dependencies.State('League', 'value'),
     dash.dependencies.State('HomeTeam', 'value'),
     dash.dependencies.State('AwayTeam', 'value')])
def update_result(n_clicks, year, league, hometeam, awayteam):
    # filter the dataframe based on the values from the dropdowns
    filtered_df = data.copy()
    if year is not None:
        filtered_df = filtered_df[filtered_df['Year'] == year]
    if league is not None:
        filtered_df = filtered_df[filtered_df['League'] == league]
    if hometeam is not None:
        filtered_df = filtered_df[filtered_df['HomeTeam'] == hometeam]
    if awayteam is not None:
        filtered_df = filtered_df[filtered_df['AwayTeam'] == awayteam]

    # return the result div with the filtered dataframe

    records = filtered_df.to_dict('records')
    columns = [{'name': i, 'id': i} for i in filtered_df.columns]

    return dash_table.DataTable(data=records, columns=columns)
 

# callback that changes the options of the HomeTeam dropdown based on the selected League
@app.callback(
    dash.dependencies.Output('HomeTeam', 'options'),
    dash.dependencies.Output('AwayTeam', 'options'),
    [dash.dependencies.Input('League', 'value')])
def update_hometeam(league):
    # filter the dataframe based on the selected league
    filtered_df = data.copy()
    if league is not None:
        filtered_df = filtered_df[filtered_df['League'] == league]

    # return the options of the HomeTeam dropdown
    return [{'label': i, 'value': i} for i in filtered_df['HomeTeam'].unique()], [{'label': i, 'value': i} for i in filtered_df['HomeTeam'].unique()]


# callback for the most goals league button
@app.callback(
    dash.dependencies.Output('results-league', 'children'),
    [dash.dependencies.Input('most-goals-league', 'n_clicks')],
    [dash.dependencies.State('Year', 'value')])
def update_most_goals_league(n_clicks, year):
    # filter the dataframe based on the selected year
    filtered_df = data.copy()
    if year is not None:
        filtered_df = filtered_df[filtered_df['Year'] == year]

    # Home Goals
    # group the dataframe by league and sum the goals
    grouped_df = filtered_df.groupby('League')['HomeGoals'].sum().reset_index()

    # get the league with the most goals
    most_goals_league = grouped_df[grouped_df['HomeGoals'] == grouped_df['HomeGoals'].max()]['League'].values[0]

    # Away Goals
    # group the dataframe by league and sum the goals
    grouped_df_away = filtered_df.groupby('League')['AwayGoals'].sum().reset_index()

    # get the league with the most goals
    most_goals_league_away = grouped_df_away[grouped_df_away['AwayGoals'] == grouped_df_away['AwayGoals'].max()]['League'].values[0]

    # return the result div with the league that has the most goals with the number of goals
    return html.Div(
        [
            html.P(f"League with the most home goals: {most_goals_league}"),
            html.P(f"Number of goals: {grouped_df['HomeGoals'].max()}"),
            html.P(f"League with the most away goals: {most_goals_league_away}"),
            html.P(f"Number of goals: {grouped_df_away['AwayGoals'].max()}")
        ]
    )


# callback for the most goals league button
@app.callback(
    dash.dependencies.Output('results-team', 'children'),
    [dash.dependencies.Input('most-goals-team', 'n_clicks')],
    [dash.dependencies.State('League', 'value'),
     dash.dependencies.State('Year', 'value')])
def update_most_goals_team(n_clicks,league, year):
    # filter the dataframe based on the selected year
    filtered_df = data.copy()

    if league is not None:
        filtered_df = filtered_df[filtered_df['League'] == league]

    if year is not None:
        filtered_df = filtered_df[filtered_df['Year'] == year]
    
    # Home Goals
    # group the dataframe by league and sum the goals
    grouped_df = filtered_df.groupby('HomeTeam')['HomeGoals'].sum().reset_index()

    # get the league with the most goals
    most_goals_team = grouped_df[grouped_df['HomeGoals'] == grouped_df['HomeGoals'].max()]['HomeTeam'].values[0]

    # Away Goals
    # group the dataframe by league and sum the goals
    grouped_df_away = filtered_df.groupby('AwayTeam')['AwayGoals'].sum().reset_index()

    # get the league with the most goals
    most_goals_team_away = grouped_df_away[grouped_df_away['AwayGoals'] == grouped_df_away['AwayGoals'].max()]['AwayTeam'].values[0]

    # return the result div with the league that has the most goals with the number of goals
    return html.Div(
        [
            html.P(f"Team with the most home goals: {most_goals_team}"),
            html.P(f"Number of goals: {grouped_df['HomeGoals'].max()}"),
            html.P(f"Team with the most away goals: {most_goals_team_away}"),
            html.P(f"Number of goals: {grouped_df_away['AwayGoals'].max()}")
        ]
    )




if __name__ == "__main__":
    app.run_server(debug=True)
