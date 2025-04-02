import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

#Dataset

fifa_df = pd.DataFrame({
    "Year": [1930,1934,1938,1950,1954,1958,1962,1966,1970,1974,1978,1982,1986,1990,1994,1998,2002,2006,2010,2014,2018,2022],
    "Winners": ["Uruguay","Italy","Italy","Uruguay","West Germany","Brazil","Brazil","England","Brazil","West Germany","Argentina","Italy","Argentina","West Germany","Brazil","France","Brazil","Italy","Spain","Germany","France","Argentina"],
    "Runners-up":["Argentina","Czechoslovakia","Hungary","Brazil","Hungary","Sweden","Czechoslovakia","West Germany","Italy","Netherlands","Netherlands","West Germany","West Germany","Argentina","Italy","Brazil","Germany","France","Netherlands","Argentina","Croatia","France"]
})

fifa_df.replace({
          'Winners': {'West Germany': 'Germany'}, 
          'Runners-up': {'West Germany': 'Germany'}
        }, 
      inplace=True
    )

winner_counts = fifa_df["Winners"].value_counts().reset_index()
winner_counts.columns = ["Country", "Wins"]

fig = px.choropleth(
    winner_counts, 
    locations='Country', 
    locationmode='country names',
    color='Wins',
    title='World Cup Wins by Country',
    color_continuous_scale=px.colors.sequential.Plasma
)
fig.update_layout(
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showocean=True,
            oceancolor="lightblue"
        ),
        margin = {"r":0,"t":0,"l":0,"b":0}
    )

app = dash.Dash(__name__)
server = app.server
default_year = fifa_df['Year'][0]
default_country = winner_counts["Country"][0]

app.layout = html.Div([
    html.H1("FIFA World Cup Winners Dashboard",  style={'textAlign': 'center', 'fontSize': 40}),
    dcc.Graph(figure=fig),
    
    html.P("Select a Country:", style={'fontSize': 20, "font-weight": "bold"}),
    dcc.Dropdown(
        id='country-list',
        options=[{'label': c, 'value': c} for c in winner_counts['Country']],
        value=default_country,
        clearable=False
    ),
    html.Div(id='total-wins', style={'textAlign': 'center'}),
    
    html.P("Select a Year:", style={'fontSize': 20}),
    dcc.Dropdown(
        id='year-list',
        options=[{'label': y, 'value': y} for y in fifa_df['Year']],
        value=default_year,
        clearable=False
    ),
    html.Div(id='yearly-result', style={'textAlign': 'center'})
])

@app.callback(
    Output('total-wins', 'children'),
    Input('country-list', 'value')
)
def total_wins(country):
    wins = winner_counts.loc[winner_counts['Country'] == country, 'Wins'].values[0]
    return html.H3(f"{country} has won the FIFA World Cup {wins} times")

@app.callback(
    Output('yearly-result', 'children'),
    Input('year-list', 'value')
)
def display_results(year):
    row = fifa_df[fifa_df['Year'] == year].iloc[0]
    return html.H3(f"Stats for FIFA world cup {year} -- Winner: {row['Winners']}, and Runner-Up: {row['Runners-up']}")

app.run(debug=True)
