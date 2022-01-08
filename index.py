

import plotly.express as px
import plotly
import plotly.io as pio
pio.renderers.default = 'browser'

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import pandas as pd


def pop_per_country(df: pd.DataFrame):
    # after we filter year, there will be only one row per year per country
    # split-apply-combine is left for potential future use
    # same apply for other charts
    dff: pd.DataFrame = df[['country', 'pop']].groupby(by='country').mean()
    dff.reset_index(inplace=True)

    fig = px.bar(
        x=dff['country'],
        y=dff['pop']
    )

    return fig


def life_exp_per_country(df: pd.DataFrame):
    dff: pd.DataFrame = df[['country', 'lifeExp']].groupby(by='country').mean()
    dff.reset_index(inplace=True)

    fig = px.bar(
        x=dff['country'],
        y=dff['lifeExp']
    )

    return fig


def gdp_perCapita_per_country(df: pd.DataFrame):
    dff: pd.DataFrame = df[['country', 'gdpPercap']].groupby(by='country').mean()
    dff.reset_index(inplace=True)

    fig = px.bar(
        x=dff['country'],
        y=dff['gdpPercap'],
        hover_name=dff['country']
    )

    return fig


def scatter_plot(df: pd.DataFrame):

    fig = px.scatter(

        y=df['lifeExp'],
        x=df['gdpPercap'],
        hover_name=df['country']
    )

    fig.update_layout(
        yaxis_title='Life expectancy',
        xaxis_title='GDP per capita'
    )

    return fig


app = dash.Dash(name=__name__)

df = plotly.data.gapminder()


app.layout = html.Div([

    html.H1('Quick exploration of gapminder dataset', style={'textAlign': 'center', 'backgroundColor':'#F0F0F0'}),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    dcc.Dropdown(
        id='dropdown-continent',
        options=[{'label': i, 'value': i} for i in df['continent'].unique()],
        value=df['continent'].unique()[0]

    ),

    html.Br(),
    html.Br(),

    dcc.Dropdown(
        id='dropdown-year',
        options=[{'label': i, 'value': i} for i in df['year'].unique().tolist()],
        value=df['year'].unique()[0]
    ),

    html.Br(),
    html.Br(),

    html.H3('Population per country', style={'textAlign': 'center', 'backgroundColor':'#F0F0F0'}),
    dcc.Graph(id='graph-population_per_country'),

    html.H3('Life expectancy per country', style={'textAlign': 'center', 'backgroundColor':'#F0F0F0'}),
    dcc.Graph(id='graph-life_exp_per_country'),

    html.H3('GDP per capita per country', style={'textAlign': 'center', 'backgroundColor':'#F0F0F0'}),
    dcc.Graph(id='graph-gdpPerCapita_per_country'),

    html.H3('Life expectancy VS GDP per capita', style={'textAlign': 'center', 'backgroundColor':'#F0F0F0'}),
    dcc.Graph(id='graph-scatter_plot')


])


@app.callback(
    [Output(component_id='graph-population_per_country', component_property='figure'),
     Output(component_id='graph-life_exp_per_country', component_property='figure'),
     Output(component_id='graph-gdpPerCapita_per_country', component_property='figure'),
     Output(component_id='graph-scatter_plot', component_property='figure')],

    [Input(component_id='dropdown-continent', component_property='value'),
     Input(component_id='dropdown-year', component_property='value')]
)
def main_data_function(continent_, year_):

    dff = df.query(expr='continent == @continent_ and year == @year_')

    fig_population = pop_per_country(df=dff)

    fig_life_expectancy = life_exp_per_country(df=dff)

    fig_gdp_perCapita = gdp_perCapita_per_country(df=dff)

    fig_scatter_plot = scatter_plot(df=dff)

    return fig_population, fig_life_expectancy, fig_gdp_perCapita, fig_scatter_plot


if __name__ == '__main__':
    app.run_server()



