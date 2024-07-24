import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, callback_context, State
from dash import html
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
from dash_bootstrap_templates import ThemeChangerAIO, ThemeSwitchAIO
from dash_bootstrap_templates import template_from_url
from pymongo import MongoClient
    

client = MongoClient("mongodb+srv://magnusfelinto:magnusmv123@cluster0.fphqfh4.mongodb.net/") 
db     = client["test"]
collection = db.get_collection("posters")
#Pegar todos os dados

response = collection.find("")
lista = list(response)

mongo_df = pd.DataFrame(lista)
#for registry in response: print(registry)


# Carregue seus dados fictícios
df = pd.read_csv("dados_ficticios_dados.csv", sep=",")

estilos = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://fonts.googleapis.com/icon?family=Material+Icons",
    dbc.themes.LUX,
]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"

app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])

df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")

app.config["suppress_callback_exceptions"] = True
app.scripts.config.serve_locally = True
server = app.server

theme_changer_id = "theme-changer"

template = dbc.themes.BOOTSTRAP
template2 = dbc.themes.CYBORG

# Criação da barra lateral
sidebar = dbc.Col(
    [
        html.H2("DashBoard", className="text-primary"),
        html.P("By CIVIS", className="text-info"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Visão Geral", href="/", active="exact", id="navlink-graph",style={"fontWeight": "bold"}),
                dbc.NavLink("Conduta dos Reportes", href="/visao_orcamento", active="exact", id="navlink-orcamento",style={"fontWeight": "bold"}),
                dbc.NavLink("Prioridades", href="/pagina1", active="exact", id="navlink-pagina1",style={"fontWeight": "bold"}),
                dbc.NavLink("Quantidade VS Qualidade", href="/pagina2", active="exact", id="navlink-pagina2",style={"fontWeight": "bold"}),
                dbc.NavLink("Visão Orçamentaria", href="/pagina3", active="exact", id="navlink-pagina3",style={"fontWeight": "bold"}),
                dbc.NavLink("Página 4", href="/pagina4", active="exact", id="navlink-pagina4",style={"fontWeight": "bold"}),
                dbc.NavLink("Página 5", href="/pagina5", active="exact", id="navlink-pagina5",style={"fontWeight": "bold"}),

                # Adicione o componente ThemeSwitchAIO à barra lateral
                dbc.Row(
                    dbc.Col(
                        ThemeSwitchAIO(
                            aio_id="theme-switch", themes=[template, template2]
                        )
                    )
                ),  
            ],
            vertical=True,
            pills=True,
            id="sidebar",
        ),
    ],
    id="sidebar_completa",
)

# Callback para atualizar o estilo dos links de navegação com base no tema selecionado
@app.callback(
    Output("navlink-graph", "style"),
    Output("navlink-orcamento", "style"),
    Output("navlink-pagina1", "style"),
    Output("navlink-pagina2", "style"),
    Output("navlink-pagina3", "style"),
    Output("navlink-pagina4", "style"),
    Output("navlink-pagina5", "style"),
    Input("theme-switch", "value")
)
def update_navlink_style(theme):
    if theme == dbc.themes.LUX:
        return {"backgroundColor": "transparent", "color": "white", "fontWeight": "bold"} * 7
    elif theme == dbc.themes.CYBORG:
        return {"backgroundColor": "transparent", "color": "white", "fontWeight": "bold"} * 7
    # Adicione mais condições para outros temas, se necessário
    else:
        # Retorne o estilo padrão
        return {"backgroundColor": "transparent", "color": "white", "fontWeight": "bold"} * 7


# Layout principal com a barra lateral
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Location(id="url"),
                        sidebar,
                        # Adicione o componente ThemeChangerAIO
                        ThemeChangerAIO(
                            aio_id=theme_changer_id,
                            radio_props={"value": dbc.themes.BOOTSTRAP},
                        ),
                    ],
                    md=2,
                ),
                dbc.Col(
                    [
                        html.Div(id="page_content"),
                    ],
                    md=10,
                ),
            ]
        ),
    ],
    fluid=True,
)




# Callback para atualizar o conteúdo da página
@app.callback(Output("page_content", "children"), [Input("url", "pathname")])
def render_page(pathname):
    if pathname == "/":
        return graph_layout()
    elif pathname == "/visao_orcamento":
        return visao_orcamento_layout()
    elif pathname == "/pagina1":
        return pagina1_layout()
    elif pathname == "/pagina2":
        return pagina2_layout()
    elif pathname == "/pagina3":
        return pagina3_layout()
    elif pathname == "/pagina4":
        return pagina4_layout()
    elif pathname == "/pagina5":
        return pagina5_layout()
    else:
        return html.P("404 - Página não encontrada.")

# Layout para a página de gráfico
def graph_layout():
    return dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dcc.Dropdown(
                                id="drop",
                                options=[
                                    {"label": location, "value": location}
                                    for location in mongo_df["categoria"].unique()
                                ],
                                placeholder="Selecione um bairro",
                                style={ 
                                    "background-color": "transparent",
                                    "color": "black",
                                    "marginLeft": "10px",  # Adicionado
                                },
                            ),
                            style={
                                "width": "100%",
                                "padding": "10px",
                                "margin": "0px",
                                "marginTop": "5px",
                                "paper_bgcolor": "rgba(0,0,0,0)",
                                "plot_bgcolor": "rgba(0,0,0,0)",
                                "background-color": "transparent",
                            },
                        ),
                        width=4,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(id="grafico"),
                            style={
                                "width": "88%",
                                "maxWidth": "550px",
                                "height": "370px",
                                "padding": "0px 10px",
                                "margin": "10px 0px",
                                "marginTop": "5px",
                            },
                        ),
                        width=5,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(id="map"),
                            style={
                                "width": "100%",
                                "padding": "0px",  # Corrigido
                                "margin": "5px",
                                #"marginTop": "0px",
                                "maxWidth": "800px",
                                "height": "370px",
                            },
                        ),
                        width=7,
                    ),
                ]
            ),
        ]
    )



# Layout para a página VISAO ORCAMENTO
def visao_orcamento_layout():
    return dbc.Col(
        [
            dbc.Row(
                
                [
                    dbc.Col(
                       
                        [
                            
                            html.H6("Período", style={"margin-top": "10px", "background-color":"transparent"}),
                           
                            dcc.DatePickerRange(
                                display_format='DD/MM/YYYY',
                                end_date_placeholder_text='Data...',
                                start_date=None,
                                end_date=None,
                                with_portal=True,
                                updatemode='singledate',
                                id='date-config',  
                                calendar_orientation='vertical',
                                clearable=True,
                                style={'backgroundColor': 'transparent'}
                            )

                        ]
                          
                    ),  
                     
                    dbc.Col(
                        [
                            dbc.Card(
                                [dcc.Dropdown(id='drop-problem',
                                              options=[
                                                  {"label": location, "value": location}
                                                  for location in mongo_df["categoria"].unique()
                                              ],
                                              placeholder="Selecione um problema",
                                              style={
                                                  "width": "100%", 
                                                  "background-color":"transparent",
                                                  "color": "black"
                                              }
                                )]
                            ),
                        ],
                        width=5
                    )
                ],
                style={"height": "100%", "padding": "20px"}
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(id="lineGraf"),
                            style={
                                "width": "100%",
                                "padding": "16px",
                                "margin": "0px",
                                "marginTop": "5px",
                                "height": "460px",
                                "maxWidth": "600px",
                                #"padding-top": "40px",
                            },
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(id="radio"),
                            style={
                                "width": "100%",
                                "padding": "16px",
                                "margin": "0px",
                                "marginTop": "5px",
                                "height": "460px",
                                "maxWidth": "600px",
                            },
                        ),
                        width=6,
                    ),
                ]
            ),

        ]
    )



# Funções para outras páginas
def pagina1_layout():
    return dbc.Col(
        [
            html.Div([
                html.Button("Resetar Filtros", id="reset-button", n_clicks=None,style={
                        'backgroundColor': "transparent",  # Cor de fundo
                        'color': "GRAY",  # Cor do texto
                        'padding': '10px 20px',  # Espaçamento interno
                        'borderRadius': '30px',  # Borda arredondada
                        'fontWeight': 'bold',
                        'cursor': 'pointer',
                        #"width": "10%",
                        "marginTop": "5px",
                }),
            ]),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(id="text", figure=line_graf_text()),
                            style={
                                "width": "100%",
                                "height": "500px",
                                "padding": "10px",
                                "margin": "0px",
                                "marginTop": "5px",
                            },
                        ),
                        width=12,
                    ),
                ],style={"height": "100%", "padding": "20px"}
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(id="bar-garf", figure=bar_chart_graph()),
                            style={
                                "width": "100%",
                                "height": "500px",
                                "padding": "10px",
                                "margin": "0px",
                                "marginTop": "5px",
                            },
                        ),
                        width=12,
                    ),
                ],style={"height": "100%", "padding": "20px"}
            )
        ]
    )

def pagina2_layout():
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dcc.Dropdown(id='dropbt4',
                                     options=[
                                         {"label": location, "value": location}
                                         for location in df["TIPO DO PROBLEMA"].unique()
                                     ],
                                     placeholder="Selecione um problema",
                                     style={
                                         "width": "100%",  
                                         "background-color":"transparent",
                                         "color": "black"
                                     },
                                    #multi=True  # Permitindo seleção múltipla
                                     )
                    ), width=5
                ),

                dbc.Col(
                    [
                        dcc.DatePickerRange(
                            display_format='DD/MM/YYYY',
                            end_date_placeholder_text='Data...',
                            start_date=None,
                            end_date=None,
                            with_portal=False,
                            updatemode='singledate',
                            id='date-config',
                            calendar_orientation='vertical',
                            clearable=True,
                             style={
                                "width": "100%",
                                "height": "100px",
                                "padding": "0px",
                                "margin": "0px",
                                "marginTop": "10px",
                                "margin-left": "150px",
                            },  
                        )
                    ],width=6
                
                ),  
            ]),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(id='bar-bt4', figure=chart_line_graphic(df)),
                            style={
                                "width": "100%",
                                "height": "450px",
                                "padding": "10px",
                                "margin": "0px",
                                "marginTop": "5px",
                                "maxWidth": "1235px",
                            },
                        ),
                        width=12,
                    ),
                ]
            ),
            #dbc.Row(
            #    [
            #        dbc.Col(
            #            dbc.Card(
            #                dcc.Graph(id='radiobt4'),
            #                style={
            #                    "width": "100%",
            #                    "height": "450px",
            #                    "padding": "5px",
            #                    "margin": "0px",
            #                    "marginTop": "5px",
            #                    "maxWidth": "600px",
            #                },
            #            ),
            #            width=6,
            #        ),
            #        dbc.Col(
            #            dbc.Card(
            #                dcc.Graph(id='radiobutton4'),
            #                style={
            #                    "width": "100%",
            #                    "height": "450px",
            #                    "padding": "5px",
            #                    "margin": "0px",
            #                    "marginTop": "5px",
            #                    "maxWidth": "600px",
            #                },
            #            ),
            #            width=6
            #        ),
            #    ]
            #)
        ]
    )



def pagina3_layout():
    return dbc.Col(
        [

            dbc.Row([
                    dbc.Col([
                           
                        dcc.DatePickerRange(
                            display_format='DD/MM/YYYY',
                            end_date_placeholder_text='Data...',
                            start_date=None,
                            end_date=None,
                            with_portal=True,
                            updatemode='singledate',
                            id='date-config',  
                            calendar_orientation='vertical',
                            clearable=True,
                            style={'backgroundColor': 'transparent'}  # Define a cor de fundo do calendário aqui
                            )

                        ]
                          
                    ),
                ]
            ),  
            # Botão para resetar filtros
            html.Div([
                html.Button("Resetar Filtros", id="button", n_clicks=None,style={
                        'backgroundColor': "transparent",  # Cor de fundo
                        'color': "GRAY",  # Cor do texto
                        'padding': '10px 20px',  # Espaçamento interno
                        'borderRadius': '30px',  # Borda arredondada
                        'fontWeight': 'bold',
                        'cursor': 'pointer',
                        #"width": "10%",
                        "marginTop": "5px",
                }),
            ]),
            # Linha com os gráficos
            dbc.Row(
                [
                    # Gráfico de pizza
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(id='chart_pie'),
                            style={
                                "width": "100%",
                                "height": "450px",
                                "padding": "10px",
                                "margin": "0px",
                                "marginTop": "5px",
                                "maxWidth": "500px",
                                "marginLeft": "20px",
                            },
                        ),
                        width=6, 
                    ),
                    # Gráfico de linhas com ID "oscilacao"
                    #dbc.Col(
                    #    dbc.Card(
                    #        dcc.Graph(id='oscilacao'),
                    #        style={
                    #            "width": "95%",
                    #            "height": "280px",  # Altura inicial definida
                    #            "padding": "10px",
                    #            "margin": "0px",
                    #            "marginTop": "5px",
                    #            "marginLeft": "0px",
                    #        },
                    #    ),
                    #    width=6,
                        
                    #),
                ],
                style={"height": "100%", "padding": "20px"}
            ),
        ]
    )

def pagina4_layout():
    return dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            # Conteúdo da Página 4
                            html.P("Conteúdo da Página 4"),
                            style={
                                "width": "100%",
                                "padding": "10px",
                                "margin": "0px",
                                "marginTop": "5px",
                            },
                        ),
                        width=6,
                    ),
                ]
            )
        ]
    )

def pagina5_layout():
    return dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            # Conteúdo da Página 5
                            html.P("Conteúdo da Página 5"),
                            style={
                                "width": "100%",
                                "padding": "10px",
                                "margin": "0px",
                                "marginTop": "5px",
                            },
                        ),
                        width=6,
                    ),
                ]
            )
        ]
    )
    
    
#Template= [
#"white",
#"flatly",
#"darkly",
#"cerulean",
#"journal",
#"lumen",
#"paper",
#"cosmo",
#"cyborg",
#"grid",
#"minty",
#"lux",
#"pulse",
#"sandstone",
#"simplex",
#"slate",
#"solar",
#"spacelab",
#"superhero",
#"united",
#"yeti",
#"minty",
#"vapor",
#   ] 
    
    

# Layout
#===============================CALLBACK 1º BOTÃO======================================================
@app.callback([Output("grafico", "figure"), Output("map", "figure")],
              [Input("drop", "value")])
def update_figure(select):
    mongo_df[['lat', 'lon']] = mongo_df[["latitude", "longitude"]]
    mongo_df['lat'] = mongo_df['lat'].str.rstrip(',')
    mongo_df['lon'] = mongo_df['lon'].str.rstrip(',')
    mongo_df['lat'] = pd.to_numeric(mongo_df['lat'])
    mongo_df['lon'] = pd.to_numeric(mongo_df['lon'])
    seu_dataframe = pd.DataFrame({
        'latitude': [-5.1874],
        'longitude': [-37.3446]
    })
    fig_map = create_map_figure(mongo_df, seu_dataframe, template="cyborg")
    estilo = dict(l=25, r=25, t=25, b=0)
    fig_map.update_layout(margin=estilo, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    

    if select is None:
        fig = create_pie_chart(mongo_df, template="cyborg")
        return fig, fig_map
    else:
        filtered_df = mongo_df[mongo_df["categoria"] == select]
        fig = create_pie_chart(filtered_df, select, template="cyborg")
        fig_map_select = create_map_figure(filtered_df, seu_dataframe, template="cyborg")
        fig.update_layout(transition_duration=100, height=390)
        return fig, fig_map_select


def create_pie_chart(data, bairro_selecionado=None, template=None):
    if bairro_selecionado:  
        title = f"Problemas em {bairro_selecionado}"
    else:
        title = "PROBLEMAS" 

    fig_line = px.pie(data, names="categoria", title=title, hole=0.3, template=template)
    estilo = dict(l=50, r=50, t=50, b=60)
    fig_line.update_layout(margin=estilo, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig_line


def create_map_figure(data, seu_dataframe, template=None):
    fig_map = px.scatter_mapbox(seu_dataframe, lat='latitude', lon='longitude', zoom=10)
    fig_map.add_trace(px.scatter_mapbox(data, lat='lat', lon='lon', zoom=10).data[0])
    design = dict(l=20, r=20, t=20, b=0)
    fig_map.update_layout(mapbox_style="open-street-map", margin=design, height=360)
    return fig_map





#===============================CALLBACK 2º BOTÃO======================================================

@app.callback(
    [Output("lineGraf", "figure"), Output("radio", "figure")],
    [Input("drop-problem", "value"), Input("date-config", "start_date"), Input("date-config", "end_date")]
)
def time_running(select_data, start_date, end_date):

    # Se todas as seleções são None, retorna os gráficos sem filtros
    if select_data is None and start_date is None and end_date is None:
        return create_line_chart(df), create_radar_chart(df)#, more_radar_chart(df)# more_line_chart(df),

    try:
        # Certifique-se de converter as datas para objetos datetime
        start_date = datetime.strptime(start_date.split(' ')[0], '%Y-%m-%d') if start_date else None
        end_date = datetime.strptime(end_date.split(' ')[0], '%Y-%m-%d') if end_date else None

        # Filtra o DataFrame com base nas datas selecionadas
        if start_date and end_date:
            filtered_df = df[(df['DATA'] >= start_date) & (df['DATA'] <= end_date)]
        else:
            filtered_df = df.copy()

        # Se houver uma seleção na dropdown, filtra ainda mais
        if select_data is not None:
            filtered_df = filtered_df[filtered_df['TIPO DO PROBLEMA'] == select_data]

        # Cria o gráfico de radar usando a função create_radar_chart
        fig_radar = create_radar_chart(filtered_df)
        fig_line = create_line_chart(filtered_df)
        #line = more_line_chart(filtered_df)
        #radar =  more_radar_chart(filtered_df)

        return fig_line, fig_radar,# radar #,line

    except Exception as e:
        print(f"Erro no callback: {e}")
        # Se ocorrer algum erro, retorna gráficos padrão
        return px.line(), px.line(), px.line() #,px.line()
        
def create_line_chart(data):
        aggregated_data = data.groupby(['DATA', 'TIPO DO PROBLEMA'])['NÚMERO DE LIKES'].sum().reset_index()
        fig_line=px.line(aggregated_data, x='DATA', y='NÚMERO DE LIKES', color='TIPO DO PROBLEMA', title='Likes ao decorrer do tempo', template="cyborg")

        estilo = dict(l=40, r=40, t=40, b=40)
        fig_line.update_layout(margin= estilo)
        fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

        return fig_line

#def more_line_chart(data):
#        df_soma = data.groupby('DATA')['NÚMERO DE PESSOAS PROXIMAS'].sum().reset_index()
#        line = px.line(df_soma, x='DATA', y='NÚMERO DE PESSOAS PROXIMAS', title='Numero de Reportação de acordo com o tempo',template="cyborg")
#        estilo = dict(l=40, r=40, t=40, b=40)
#        line.update_layout(margin= estilo)
#        line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
#        return line


def create_radar_chart(data):
    categories = data["TIPO DO PROBLEMA"].unique()
    soma_marcações = data.groupby("TIPO DO PROBLEMA")["NÚMERO DE MARCAÇÕES FEITAS"].sum()
    soma_likes = data.groupby("TIPO DO PROBLEMA")["NÚMERO DE LIKES"].sum()

    radar_fig = go.Figure()

    radar_fig.add_trace(go.Scatterpolar(
        r=soma_marcações,
        theta=categories,
        fill='toself',
        name='SOMA DE MARCAÇÕES FEITAS',
        line=dict(color='blue'), 
        
    ))

    radar_fig.add_trace(go.Scatterpolar(
        r=soma_likes,
        theta=categories,
        fill='toself',
        name='SOMA DE NUMERO DE LIKES',
        line=dict(color='red')
    ))

    estilo = dict(l=40, r=40, t=40, b=40)
    radar_fig.update_layout(
        margin=estilo,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title="Indicadores de Acertividade",
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        font=dict(color="gray", size = 12)  # Definindo a cor do texto para cinza
    )

    return radar_fig


    #def more_radar_chart(data):
    #    categories1 = data["STATUS DO USUARIO"].unique()

        # Certifique-se de lidar com vírgulas e converta para float
    #    try:
    #        data["nivel de acertividade do usuario"] = data["nivel de acertividade do usuario"].str.replace(',', '.').astype(float)
    #    except AttributeError:
            # Se a coluna já for de tipo float, não precisa fazer a conversão novamente
    #        pass

    #    values1 = data.groupby("STATUS DO USUARIO")["nivel de acertividade do usuario"].sum()
    #    status_counts = data["STATUS DO USUARIO"].value_counts().reset_index()
    #    status_counts.columns = ["STATUS DO USUARIO", "Contagem"]

        # Certifique-se de lidar com valores nulos ou NaN após a conversão
    #    values1.fillna(0, inplace=True)

    #    porcentagem = (values1 / values1.sum()) * 100

        # Arredonda a porcentagem para duas casas decimais
    #    porcentagem = round(porcentagem, 2)

        # Crie um objeto de figura para o gráfico de radar
    #    radar = go.Figure()

        # Adicione o trace do gráfico de radar para a série 1 com uma cor específica
    #    radar.add_trace(go.Scatterpolar(
    #        r=porcentagem,
    #        theta=categories1,
    #        fill='toself',
    #        name='% ACERTIVIDADE',
    #        line=dict(color='green')  # Defina a cor desejada (por exemplo, 'blue')
    #    ))

    #    # Adicione o trace do gráfico de radar para a série 2 com outra cor
    #    radar.add_trace(go.Scatterpolar(
    #        r=status_counts["Contagem"].tolist(),
    #        theta=status_counts["STATUS DO USUARIO"].tolist(),
    #        fill='toself',
    #        name='Quantidade de usuarios',
    #        line=dict(color='blue')
    #    ))

    #    estilo = dict(l=51, r=40, t=40, b=40)
            #radar_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'),
    #    radar.update_layout(margin=estilo,paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    #        title="Indicador de Acertividade",
    #        polar=dict(radialaxis=dict(visible=True)),
    #        showlegend=True,
    #        font=dict(color = 'gray', size = 12)
    #    )

    #    return radar


#===============================CALLBACK 3º BOTÃO======================================================
@app.callback(
    [Output("text", "figure"), Output("bar-garf", "figure")],
    [Input("text", "clickData"), Input("reset-button", "n_clicks")]
)
def choose_option(clickData, reset_clicks):
    ctx = dash.callback_context
    if ctx.triggered_id == "reset-button":
        return line_graf_text(), bar_chart_graph()
        
    elif clickData is not None:
        selected_tipo_problema = clickData["points"][0]["x"]
        filtered_df = df[df["TIPO DO PROBLEMA"] == selected_tipo_problema]
    else:
        filtered_df = df.copy()

    line_graphic = line_graf_text(filtered_df)
    bar_graphic = bar_chart_graph(filtered_df)

    if clickData is not None:
        line_graphic.add_annotation(
            text=f'Tipo Problema: {selected_tipo_problema}',
            xref='paper', yref='paper',
            x=0.95, y=0.95,
            showarrow=False,
            font=dict(size=12)
        )

    return line_graphic, bar_graphic



def line_graf_text(data=None):
    if data is None:
        data = df.copy()

    data['NÚMERO DE MARCAÇÕES FEITAS'] = pd.to_numeric(data['NÚMERO DE MARCAÇÕES FEITAS'], errors='coerce')
    df_soma_marcacoes = data.groupby(['TIPO DO PROBLEMA', 'NIVEL DE URGENCIA'])['NÚMERO DE MARCAÇÕES FEITAS'].sum().reset_index()

    graphic = px.bar(df_soma_marcacoes, x='TIPO DO PROBLEMA', y='NÚMERO DE MARCAÇÕES FEITAS', color='NIVEL DE URGENCIA', 
                    title=f'Nivel de urgencia por tipo de problema', barmode="group",  template="cyborg")
    
    estilo = dict(l=30, r=25, t=30, b=0)
    graphic.update_layout(margin= estilo)
    graphic.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    
    return graphic


def bar_chart_graph(data=None):
    if data is None:
        data = df.copy()
        
    data['DATA'] = pd.to_datetime(data['DATA'])
    consolidated_data = data.groupby(['DATA', 'TIPO DO PROBLEMA'])['NÚMERO DE MARCAÇÕES FEITAS'].sum().reset_index()

    # Crie um gráfico de área com a soma das marcações
    fig = px.line(consolidated_data, x='DATA', y='NÚMERO DE MARCAÇÕES FEITAS', color='TIPO DO PROBLEMA',  template="cyborg",
                    title='Numero de Marcações por Tipo de Problema', 
                    labels={'NÚMERO DE MARCAÇÕES FEITAS': 'Soma das Marcações'})
    
    estilo = dict(l=30, r=25, t=30, b=0)
    fig.update_layout(margin= estilo)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig



#===============================CALLBACK 4º BOTÃO======================================================

@app.callback(
    [Output("bar-bt4", "figure")],# Output("radiobt4", "figure"), Output("radiobutton4", "figure")],
    [Input("dropbt4", "value"), Input("date-config", "start_date"), Input("date-config", "end_date")]
)
def relacao_tipo_problem(drop_value, start_date, end_date):
    # Se todos os valores são None, retorna os gráficos sem filtros
    if drop_value is None and start_date is None and end_date is None:
        return chart_line_graphic(df),# chart_radio_1(df), chart_radio_2(df)
    
    try:
        # Certifique-se de converter as datas para objetos datetime
        start_date = datetime.strptime(start_date.split(' ')[0], '%Y-%m-%d') if start_date else None
        end_date = datetime.strptime(end_date.split(' ')[0], '%Y-%m-%d') if end_date else None

        # Filtra o DataFrame com base nas datas selecionadas
        if start_date and end_date:
            filtered_df = df[(df['DATA'] >= start_date) & (df['DATA'] <= end_date)]
        else:
            filtered_df = df.copy()

        # Se houver uma seleção na dropdown, filtra ainda mais
        if drop_value is not None:
            filtered_df = filtered_df[filtered_df['TIPO DO PROBLEMA'] == drop_value]

        # Cria os gráficos com o DataFrame filtrado
        graphic_bar = chart_line_graphic(filtered_df)
        #radar_fig_4 = chart_radio_1(filtered_df)
        #fig_radar = chart_radio_2(filtered_df)
        
        return graphic_bar,# radar_fig_4, fig_radar

    except Exception as e:
        print(f"Erro no callback: {e}")
        # Se ocorrer algum erro, retorna gráficos padrão
        return chart_line_graphic(df)#, chart_radio_1(df), chart_radio_2(df)





def chart_line_graphic(df):
    df['NÚMERO DE MARCAÇÕES FEITAS'] = pd.to_numeric(df['NÚMERO DE MARCAÇÕES FEITAS'], errors='coerce')
    df_sum_marcacoes = df.groupby('TIPO DO PROBLEMA')['NÚMERO DE MARCAÇÕES FEITAS'].sum().reset_index()
    

    graphic_bar = px.bar(df_sum_marcacoes, x='TIPO DO PROBLEMA', y='NÚMERO DE MARCAÇÕES FEITAS', color='TIPO DO PROBLEMA',template="cyborg",
                     title='Número de Marcações por Tipo de Problema',
                     labels={'NÚMERO DE MARCAÇÕES FEITAS': 'Número de Marcações'})
    #estilo = dict(l=30, r=25, t=30, b=0)
    #graphic_bar.update_layout(margin= estilo)
    graphic_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return graphic_bar


#def chart_radio_1(df):

    # PEGA todos os valores únicos na coluna "TIPO DO PROBLEMA"
    categories = df["TIPO DO PROBLEMA"].unique()

    df["nivel de acertividade do usuario"].fillna(0, inplace=True)
    df["NÚMERO DE LIKES"].fillna(0, inplace=True)

    # Converte as colunas para tipo numérico
    df["nivel de acertividade do usuario"] = pd.to_numeric(df["nivel de acertividade do usuario"], errors='coerce')
    df["NÚMERO DE LIKES"] = pd.to_numeric(df["NÚMERO DE LIKES"], errors='coerce')

# Extrai as somas das colunas
    soma_marcações = df.groupby("TIPO DO PROBLEMA")["nivel de acertividade do usuario"].sum()
    soma_marcações2 = df.groupby("TIPO DO PROBLEMA")["NÚMERO DE LIKES"].sum()

# Calcular percentual em relação à soma total para cada categoria
    percentual_marcações = (soma_marcações / soma_marcações.sum()) * 100
    percentual_likes = (soma_marcações2 / soma_marcações2.sum()) * 100

# Crie um objeto de figura para o gráfico de radar
    radar_fig_4 = go.Figure()

# Adicione os traces do gráfico de radar
    radar_fig_4.add_trace(go.Scatterpolar(
        r=percentual_marcações,
        theta=categories,
        fill='toself',
        name='Contagem de Acertividade',
        line=dict(color='blue')
    ))

    radar_fig_4.add_trace(go.Scatterpolar(
        r=percentual_likes,
        theta=categories,
        fill='toself',
        name='Contagem de Numero de Likes',
        line=dict(color='red')
    ))

# Atualize o layout do gráfico de radar
    radar_fig_4.update_layout(
        title="Proporção de Likes e Acertividade em %",
        polar=dict(
            radialaxis=dict(
                visible=True,
                tickfont=dict(color='gray', size=12)  # Define a cor e o tamanho da fonte dos rótulos do eixo radial
            )
        ),
        showlegend=True,
        font=dict(color='gray')  # Define a cor da legenda
    )
    estilo = dict(l=30, r=25, t=30, b=0)
    radar_fig_4.update_layout(margin=estilo)
    radar_fig_4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return radar_fig_4

#def chart_radio_2(df):
    # Converte as colunas para tipo numérico
    df["NÚMERO DE PESSOAS PROXIMAS"] = pd.to_numeric(df["NÚMERO DE PESSOAS PROXIMAS"], errors='coerce')
    df["NÚMERO DE MARCAÇÕES FEITAS"] = pd.to_numeric(df["NÚMERO DE MARCAÇÕES FEITAS"], errors='coerce')

    # Extrai as somas das colunas
    soma_pessoas_proximas = df.groupby("TIPO DO PROBLEMA")["NÚMERO DE PESSOAS PROXIMAS"].sum().reset_index(name='sum_pessoas_proximas')
    soma_marcações_feitas = df.groupby("TIPO DO PROBLEMA")["NÚMERO DE MARCAÇÕES FEITAS"].sum().reset_index(name='sum_marcações_feitas')

    # Crie um objeto de figura para o gráfico de radar
    fig_radar = go.Figure()

    # Adicione os traces do gráfico de radar
    fig_radar.add_trace(go.Scatterpolar(
        r=soma_pessoas_proximas["sum_pessoas_proximas"],
        theta=soma_pessoas_proximas["TIPO DO PROBLEMA"],
        fill='toself',
        name='NÚMERO DE PESSOAS PROXIMAS',
        line=dict(color='black')
    ))

    fig_radar.add_trace(go.Scatterpolar(
        r=soma_marcações_feitas["sum_marcações_feitas"],
        theta=soma_marcações_feitas["TIPO DO PROBLEMA"],
        fill='toself',
        name='NÚMERO DE MARCAÇÕES FEITAS',
        line=dict(color='red')
    ))

    # Atualize o layout do gráfico de radar
    fig_radar.update_layout(    
        title="Proporção de Nº Marcações e de Acertividade em %",
        polar=dict(
            radialaxis=dict(
                visible=True,
                tickfont=dict(color='gray', size=12)  # Define a cor e o tamanho da fonte
            )
        ),
        showlegend=True,
        font=dict(color='gray')  # Define a cor da legenda
    )
    estilo = dict(l=30, r=25, t=30, b=0)
    fig_radar.update_layout(margin=estilo)
    fig_radar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    

    return fig_radar





#================================================BOTÃO º5===========================================================


@app.callback(
    [Output("chart_pie", "figure")], #Output("oscilacao", "figure")],
    [Input("chart_pie", "clickData"), Input("button", "n_clicks"), Input("date-config", "start_date"), Input("date-config", "end_date")]
)
def option(clickData, reset_clicks, start_date, end_date):
    ctx = dash.callback_context
    if ctx.triggered_id == "button":
        return pie_chart(mongo_df), #linhas_graf(mongo_df)
        
    elif clickData is not None and clickData["points"]:
        selected_tipo_problema = clickData["points"][0]["label"]
        filtered_df = mongo_df[mongo_df["categoria"] == selected_tipo_problema]
    else:
        filtered_df = mongo_df.copy()

    # Filtrar o DataFrame com base nas datas selecionadas
    if start_date and end_date:
        start_date = datetime.strptime(start_date.split(' ')[0], '%Y-%m-%d')
        end_date = datetime.strptime(end_date.split(' ')[0], '%Y-%m-%d')
        # Filtrar o DataFrame original com base nas datas selecionadas
        filtered_df = mongo_df[(mongo_df['postdate'] >= start_date) & (mongo_df['postdate'] <= end_date)]

        # Contar o número de ocorrências de cada tipo de problema no DataFrame filtrado
        contagem_problemas = filtered_df['categoria'].value_counts()

        # Criar o gráfico de pizza com as contagens de problemas
        pie_graphic = px.pie(names=contagem_problemas.index, values=contagem_problemas.values)

        estilo = dict(l=40, r=40, t=40, b=0)
        pie_graphic.update_layout(margin=estilo)
        pie_graphic.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    else:
        # Se as datas não estiverem selecionadas, criar o gráfico de pizza padrão com todos os problemas
        pie_graphic = pie_chart(mongo_df)

    #linhas = linhas_graf(mongo_df)

    if clickData is not None and clickData["points"]:
        tipo_problema_label = f"Tipo de problema: {selected_tipo_problema}"
        pie_graphic.add_annotation(
            text=tipo_problema_label,
            xref='paper', yref='paper',
            x=0.5, y=1.1,
            showarrow=False,
            font=dict(size=20)
        )

    return pie_graphic, #linhas


def pie_chart(mongo_df):
    contagem = mongo_df['categoria'].value_counts()
    grafo = px.pie(mongo_df, names=contagem.index, values=contagem.values, hole=0.4, template="cyborg")
    
    estilo = dict(l=50, r=50, t=50, b=50)
    grafo.update_layout(margin=estilo)
    grafo.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return grafo

#def linhas_graf(df):
    df_soma = df.groupby('DATA').agg({
        'RECEITA ETIMADA ': 'sum',
        'RECEITA DISPONIVEL': 'sum',
        'RECEITA APLICADA': 'sum'
    }).reset_index()

    # Definir a altura desejada para o gráfico

    linhag = px.line(df_soma, x='DATA', y=['RECEITA ETIMADA ', 'RECEITA APLICADA', 'RECEITA DISPONIVEL'], template="cyborg",
                     title='Oscilação da Receita com o Tempo',
                     labels={'value': 'Receita', 'variable': 'Tipo de Receita'})

    # Ajustar a altura do gráfico
    linhag.update_layout(height=260)


    estilo = dict(l=40, r=40, t=40, b=0)
    linhag.update_layout(margin= estilo)
    linhag.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    
    return linhag
    


if __name__ == "__main__":
    app.run_server(debug=True)