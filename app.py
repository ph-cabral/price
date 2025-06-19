import os
import dash
import pandas as pd
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Cargar el parquet
df = pd.read_parquet("todo.parquet")

# Inicializar app
app = dash.Dash(__name__)
app.title = "Buscador de precios"

# Layout
app.layout = html.Div([
    html.H1("🔍 Comparador de precios", style={"textAlign": "center"}),

    html.Div([
        dcc.Input(id='filtro1', placeholder='Buscar en producto (filtro 1)', type='text'),
        dcc.Input(id='filtro2', placeholder='Filtro 2', type='text'),
        dcc.Input(id='filtro3', placeholder='Filtro 3', type='text'),
    ], style={"display": "flex", "gap": "10px", "marginBottom": "20px"}),

    dash_table.DataTable(
        id='tabla',
        page_size=20,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "minWidth": "100px", "maxWidth": "300px"},
    )
])

# Callback para actualizar tabla y columnas visibles
@app.callback(
    Output('tabla', 'data'),
    Output('tabla', 'columns'),
    Input('filtro1', 'value'),
    Input('filtro2', 'value'),
    Input('filtro3', 'value'),
)
def actualizar_tabla(f1, f2, f3):
    df_filtrado = df.copy()

    # Aplicar filtros sobre columna "producto"
    for filtro in [f1, f2, f3]:
        if filtro:
            df_filtrado = df_filtrado[df_filtrado["producto"].str.contains(filtro, case=False, na=False)]

    df_filtrado = df_filtrado.loc[:, ~(df_filtrado == "").all()]

    return (
            df_filtrado.to_dict("records"),
            [{"name": i, "id": i} for i in df_filtrado.columns]
        )


# Ejecutar
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8051))
    app.run(host="0.0.0.0", port=port, debug=True)
