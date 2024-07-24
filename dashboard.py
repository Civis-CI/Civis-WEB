import dash
import dash_html_components as html

def init_dash(app):
    dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')

    dash_app.layout = html.Div([
        html.H1('Dash App Integrado com Flask'),
        html.Div('Exemplo de conteúdo do Dash.')
    ])

    return dash_app

# Permitir que o Dash seja executado separadamente para fins de desenvolvimento
if __name__ == "__main__":
    from flask import Flask
    server = Flask(__name__)
    init_dash(server)
    server.run(debug=True)