from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server
df = pd.read_csv("https://raw.githubusercontent.com/aleEco1/aplicacion/main/datos.csv")

app.layout = html.Div([
    html.H1('Sueldo promedio por profesionista en México (con licenciatura entre 20 y 30 años)', style={'textAlign': 'center', 'color': "blue", 'font-size': 30}),
    html.P('Proporción por número de profesionistas en cada estado', style={'textAlign':'center', 'color': 'black'}),

    dcc.Dropdown(
        id='dropdown',
        options=[{'label': c, 'value': c} for c in df['Descripción_Campo_amplio'].unique()],
        value='Administración y negocios', 
        style = {"width":"500px"}
    ),  

    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in sorted(df['Año'].unique())],
        value=df['Año'].min(),  # Valor inicial como el primer año
        style = {"width":"500px"}
    ),  

    dcc.Graph(id='graph'), 
    dcc.Graph(id='bar-graph'), 
    html.Label("Con datos de ENOE(INEGI). Registros con sueldos declarados", style = {"color": "black"})
])

@app.callback(
    [Output('scatter-graph', 'figure'),
     Output('bar-graph', 'figure')],
    [Input('dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_graph(selected_career, selected_year):
    # Filtro general
    filtered_df = df[df['Descripción_Campo_amplio'] == selected_career]
    
    # Figura principal
    ffig = px.scatter(
        filtered_df,
        x="Año",
        y="Sueldo promedio por profesionista",
        color="DESCRIP",
        size="fac_tri",
        size_max=25,
        template="simple_white",
        height=500,
        width=900,
        labels={"DESCRIP":"Estado", "fac_tri":"Profesionistas"}
    )
    ffig.update_xaxes(type="category")

    # Datos de Guanajuato para el mismo campo
    df_gto = df[
        (df["DESCRIP"] == "Guanajuato") &
        (df["Descripción_Campo_amplio"] == selected_career)
    ]

    # Añadir traza secundaria (puntos + flecha)
    ffig.add_trace(
        px.scatter(
            df_gto,
            x="Año",
            y="Sueldo promedio por profesionista",
            size="fac_tri",
            size_max=20,
            text=["Guanajuato"]*len(df_gto),
        ).data[0]
    )

    bar_data = filtered_df[filtered_df['Año'] == selected_year]
    bar_fig = px.bar(
        bar_data,
        x="DESCRIP",  # Estados
        y="Sueldo promedio por profesionista",  # Sueldo promedio
        color="DESCRIP",  # Colores por estado
        title=f"Sueldo Promedio por Estado en {selected_year}",
        labels={"DESCRIP": "Estado", "Sueldo promedio por profesionista": "Sueldo Promedio"},
        template="simple_white",
        height=500,
        width=900
    )
    bar_fig.update_xaxes(tickangle=45)

    # Añadir flechas (anotaciones)

    
    return ffig,bar_fig


if __name__ == '__main__':
    app.run(debug=True)