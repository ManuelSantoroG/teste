import dash
from dash import html, dcc,Input, Output, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

df = pd.read_csv("train_strokes.csv")
columnas_no_float = []

#Retirar id
df = df.drop(columns=['id'])


# Transformar os valores em float, caso possivel
for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except ValueError:
        columnas_no_float.append(col)

#Estilo da Barra lateral
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#f8f9fa",
}

CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        html.P(
            "", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Página Inicial", href="/", active="exact"),
                dbc.NavLink("Compreensão dos Dados", href="/page-1", active="exact"),
                dbc.NavLink("Análise dos Dados", href="/page-2", active="exact"),
                dbc.NavLink("Kaggle - Base de Dados", href="https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset?datasetId=1120859]", active="exact", target="_blank"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    #Página - Inicial
    if pathname == "/":
        image_path = 'assets/Logo.png'
        Logo_Pagina = html.Img(src=image_path, style={'position': 'absolute', 'top': '10px', 'right':'10px', 'height': '50px', 'width': 'auto'})
        Titulo_Pagina = html.P("Aplicação Web Baseada na Base de Dados Stroke Prediction Dataset", 
                               style={'fontWeight': 'bold', 
                                      'marginTop': '40px', 
                                      'textAlign':'center',
                                      'fontSize':'25px'}) 
        Texto_Pagina = html.P("Disponível em https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset?datasetId=1120859]",
                              style={'textAlign':'left',
                                      'fontSize':'10px'})
       
        return [ 
            Logo_Pagina,
            Titulo_Pagina,
            Texto_Pagina,
            
        ]
        
    #Página - Visualização da Tabela
    elif pathname == "/page-1":
        Titulo_Pagina_1 = html.P("Visualização da Base de Dados",
                                 style={'fontWeight': 'bold', 
                                      'textAlign':'left',
                                      'fontSize':'20px'})
        Tabela = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
        return [
            Titulo_Pagina_1,
            Tabela
        ]
    
    #Pagina - Gráficos 
    elif pathname == "/page-2":
 
 #--------------------------------------------------------#
        #TESTAR COM UMA VARIAVEL
        #Lista de Váriaveis da Nossa DB
        Variaveis = dcc.Dropdown( id='Escolha a Variável',
                     options=[{'label': col, 'value': col} for col in df.columns],
                     value=df.columns[0],  # Valor inicial 
                     style={'width': '50%'})
        
        Texto_Pagina2 = html.P("Testar Uma Variável",
                              style={'fontWeight': 'bold',
                                     'textAlign':'left',
                                      'fontSize':'15px'})

        #Titulo da Pagina com os Gráficos
        Titulo_Pagina_2=html.P("Análise de Dados",
                               style={'fontSeight': 'bold',
                                      'textAlign':'left',
                                      'fontSize':'20px'})
        
        #Apresentar o Gráfico
        Apresentar = dcc.Graph(id='histograma-dinamico')

 #--------------------------------------------------------#
        #TESTAR COM DUAS VARIAVEIS

        Texto4_Pagina2 = html.P("Testes com Duas Variáveis",
                              style={'fontWeight': 'bold',
                                     'textAlign':'left',
                                      'fontSize':'15px'})
        
        Texto2_Pagina2 = html.P("Testar a Primeira Variável",
                              style={'textAlign':'left',
                                      'fontSize':'15px'})

        #Lista de Váriaveis1 da Nossa DB
        Variaveis1 = dcc.Dropdown( id='Escolha a Primeira Variável',
                     options=[{'label': col, 'value': col} for col in df.columns],
                     value=df.columns[0],  # Valor inicial 
                     style={'width': '50%'})
        
        Texto3_Pagina2 = html.P("Testar a Segunda Variável",
                              style={'textAlign':'left',
                                      'fontSize':'15px'})

        #Lista de Váriaveis2 da Nossa DB
        Variaveis2 = dcc.Dropdown( id='Escolha a Segunda Variável',
                     options=[{'label': col, 'value': col} for col in df.columns],
                     value=df.columns[0],  # Valor inicial 
                     style={'width': '50%'})
        
        Apresentar2 = dcc.Graph(id='boxplot-dinamico')
        Apresentar3 = dcc.Graph(id='graph-dinamico')

 #--------------------------------------------------------#
        #APRESENTAR/RETORNAR TUDO NA WEB APP
        return [
            Titulo_Pagina_2,
            Texto_Pagina2,
            Variaveis,
            Apresentar,
            Texto4_Pagina2,
            Texto2_Pagina2,
            Variaveis1,
            Texto3_Pagina2,
            Variaveis2,
            Apresentar2,
            Apresentar3]

 #--------------------------------------------------------#
 # Caso, tente entrar numa página diferente, mostrar erro
    return html.Div(
        [
        html.H1("404: Not found", className="text-danger"),
        html.Hr(),
        html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


 #--------------------------------------------------------#
#CRIAÇÃO DOS GRÁFICOS

@app.callback(
    Output('histograma-dinamico', 'figure'),
    [Input('Escolha a Variável', 'value')]
    )
def update_graph(Variaveis):
    color = px.colors.qualitative.Set1[0]
    fig = px.histogram(df, 
                x=Variaveis,
                title=f'Frequência de {Variaveis}',
                color_discrete_sequence=[color],
                barmode='overlay',
                opacity=0.7,
                nbins=10)
    return fig

@app.callback(
    [Output('boxplot-dinamico', 'figure'),
    Output('graph-dinamico','figure')],
    [Input('Escolha a Primeira Variável', 'value'),
     Input('Escolha a Segunda Variável', 'value')]
    )

def update_graph2(Variaveis1, Variaveis2):
    color1 = px.colors.qualitative.Set1[0]
    
    fig2 = px.box(df, 
                  x=Variaveis1,
                  y=Variaveis2, 
                  title=f'Boxplot de {Variaveis1} por {Variaveis2}',
                  color_discrete_sequence=[color1])
    
    fig3 = px.histogram(df, 
                    x=Variaveis1,
                    facet_col=Variaveis2,
                    title=f'Frequência de {Variaveis1} por {Variaveis2}',
                    color_discrete_sequence=[color1],
                    barmode='overlay',
                    opacity=0.7,
                    nbins=10,
                    facet_col_spacing=0.005)
    return fig2, fig3

if __name__ == '__main__':
    app.run_server(debug=True)
