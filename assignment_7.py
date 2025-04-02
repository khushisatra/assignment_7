{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import dash\n",
    "from dash import dcc, html\n",
    "import plotly.express as px\n",
    "from dash.dependencies import Input, Output"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Dataset\n",
    "\n",
    "fifa_df = pd.DataFrame({\n",
    "    \"Year\": [1930,1934,1938,1950,1954,1958,1962,1966,1970,1974,1978,1982,1986,1990,1994,1998,2002,2006,2010,2014,2018,2022],\n",
    "    \"Winners\": [\"Uruguay\",\"Italy\",\"Italy\",\"Uruguay\",\"West Germany\",\"Brazil\",\"Brazil\",\"England\",\"Brazil\",\"West Germany\",\"Argentina\",\"Italy\",\"Argentina\",\"West Germany\",\"Brazil\",\"France\",\"Brazil\",\"Italy\",\"Spain\",\"Germany\",\"France\",\"Argentina\"],\n",
    "    \"Runners-up\":[\"Argentina\",\"Czechoslovakia\",\"Hungary\",\"Brazil\",\"Hungary\",\"Sweden\",\"Czechoslovakia\",\"West Germany\",\"Italy\",\"Netherlands\",\"Netherlands\",\"West Germany\",\"West Germany\",\"Argentina\",\"Italy\",\"Brazil\",\"Germany\",\"France\",\"Netherlands\",\"Argentina\",\"Croatia\",\"France\"]\n",
    "})\n",
    "\n",
    "fifa_df.replace({\n",
    "          'Winners': {'West Germany': 'Germany'}, \n",
    "          'Runners-up': {'West Germany': 'Germany'}\n",
    "        }, \n",
    "      inplace=True\n",
    "    )"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8050/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x21147b87850>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "winner_counts = fifa_df[\"Winners\"].value_counts().reset_index()\n",
    "winner_counts.columns = [\"Country\", \"Wins\"]\n",
    "\n",
    "fig = px.choropleth(\n",
    "    winner_counts, \n",
    "    locations='Country', \n",
    "    locationmode='country names',\n",
    "    color='Wins',\n",
    "    title='World Cup Wins by Country',\n",
    "    color_continuous_scale=px.colors.sequential.Plasma\n",
    ")\n",
    "\n",
    "app = dash.Dash()\n",
    "\n",
    "default_year = fifa_df['Year'][0]\n",
    "default_country = winner_counts[\"Country\"][0]\n",
    "\n",
    "app.layout = html.Div([\n",
    "    html.H1(\"FIFA World Cup Winners Dashboard\",  style={'textAlign': 'center', 'fontSize': 40}),\n",
    "    dcc.Graph(figure=fig),\n",
    "    \n",
    "    html.P(\"Select a Country:\", style={'fontSize': 20, \"font-weight\": \"bold\"}),\n",
    "    dcc.Dropdown(\n",
    "        id='country-list',\n",
    "        options=[{'label': c, 'value': c} for c in winner_counts['Country']],\n",
    "        value=default_country,\n",
    "        clearable=False\n",
    "    ),\n",
    "    html.Div(id='total-wins', style={'textAlign': 'center'}),\n",
    "    \n",
    "    html.P(\"Select a Year:\", style={'fontSize': 20}),\n",
    "    dcc.Dropdown(\n",
    "        id='year-list',\n",
    "        options=[{'label': y, 'value': y} for y in fifa_df['Year']],\n",
    "        value=default_year,\n",
    "        clearable=False\n",
    "    ),\n",
    "    html.Div(id='yearly-result', style={'textAlign': 'center'})\n",
    "])\n",
    "\n",
    "@app.callback(\n",
    "    Output('total-wins', 'children'),\n",
    "    Input('country-list', 'value')\n",
    ")\n",
    "def total_wins(country):\n",
    "    wins = winner_counts.loc[winner_counts['Country'] == country, 'Wins'].values[0]\n",
    "    return html.H3(f\"{country} has won the FIFA World Cup {wins} times\")\n",
    "\n",
    "@app.callback(\n",
    "    Output('yearly-result', 'children'),\n",
    "    Input('year-list', 'value')\n",
    ")\n",
    "def display_results(year):\n",
    "    row = fifa_df[fifa_df['Year'] == year].iloc[0]\n",
    "    return html.H3(f\"Stats for FIFA world cup {year} -- Winner: {row['Winners']}, and Runner-Up: {row['Runners-up']}\")\n",
    "\n",
    "app.run(debug=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
