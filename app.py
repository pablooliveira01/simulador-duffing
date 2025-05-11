import dash
from dash import html, dcc, Input, Output, callback_context, no_update
import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objs as go

# --- Configurações iniciais ---

app = dash.Dash(
    __name__,
    external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"],
    suppress_callback_exceptions=True
)
server = app.server

# Parâmetros default
defaults = dict(delta=0.2, alpha=1.0, beta=1.0, A=0.3, phi=1.2, epsilon=0.05,
                t_start=0, t_end=50, num_points=2000)

# Presets
presets = {
    'Ressonância Linear':                   dict(delta=0.05, alpha=1.0, beta=0.0, A=0.5, phi=1.0, epsilon=0.05),
    'Caos Bistável':                        dict(delta=0.05, alpha=-1.0, beta=1.0, A=0.35, phi=1.2, epsilon=0.05),
    'Convergência a espiral':               dict(delta=0.01, alpha=1.0, beta=1.0, A=0.25, phi=0.8, epsilon=0.05),
    'Bifurcação Homoclínica':               dict(delta=0.25, alpha=-1.0, beta=1.0, A=0.4, phi=1.0, epsilon=0.05),
    'Atrator Estranho':                     dict(delta=0.2, alpha=-1.0, beta=1.0, A=0.65, phi=1.0, epsilon=0.05),
    'Dinâmica Quase-Periódica':             dict(delta=0.1, alpha=1.0, beta=0.2, A=0.3, phi=2.5, epsilon=0.05),
    'Transição para o Caos':                dict(delta=0.15, alpha=-0.5, beta=0.5, A=0.72, phi=0.8, epsilon=0.05),
    'Ressonância Subharmônica':             dict(delta=0.08, alpha=1.0, beta=0.5, A=0.65, phi=3.0, epsilon=0.05),
    'Oscilação Amortecida':                 dict(delta=0.1, alpha=1.0, beta=1.0, A=0.0, phi=0.0, epsilon=0.05),
    'Oscilação Periódica Estável':          dict(delta=0.1, alpha=1.0, beta=1.0, A=0.3, phi=1.0, epsilon=0.05),
    'Duplicação de Período (Rota-dobra)':   dict(delta=0.3, alpha=-1.0, beta=1.0, A=0.28, phi=1.2, epsilon=0.05)
}

# Equação do Oscilador de Duffing
def duffing(t, y, δ, α, β, A, ϕ):
    x, v = y
    return [v, -δ*v - α*x - β*x**3 + A*np.cos(ϕ*t)]

# Função para resolver a equação diferencial
def solve_base(δ, α, β, A, ϕ, x0=1, v0=2):
    t = np.linspace(defaults['t_start'], defaults['t_end'], defaults['num_points'])
    sol = solve_ivp(duffing, [t[0], t[-1]], [x0, v0], t_eval=t,
                    args=(δ, α, β, A, ϕ), method='DOP853')
    return sol.t, sol.y[0], sol.y[1]

# --- Layout da Aplicação ---

app.layout = html.Div(className="p-0 m-0", children=[
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content"),
    dcc.Interval(id="splash-timer", interval=8000, n_intervals=0, max_intervals=1)  # Timer de 8s
])

# Splash screen
index_page = html.Div(className="vh-100 vw-100 d-flex flex-column justify-content-center align-items-center bg-light", children=[
    html.Img(src="/assets/cc-ufg.png", style={'height': '1000px', 'margin-bottom': '1rem'}),
    html.H1("Oscilador de Duffing", className="mb-1"),
    html.H4("Pablo Oliveira — 202103766", className="mb-4"),
    dcc.Loading(type="circle", children=html.Div("Carregando..."), style={"min-height": "50px", "min-width": "50px"})
])

# Página principal
app_page = html.Div(className="container-fluid p-0", style={'width': '95%', 'margin': '0 auto'}, children=[
    # Título
    html.Nav(className="navbar navbar-light bg-white border-bottom mb-3", children=[
        html.Div(className="container-fluid", children=[
            html.Span("Simulador do Oscilador de Duffing", className="navbar-brand mb-0 h1")
        ])
    ]),

    # Dropdown de presets
    html.Div(className="p-3 bg-white", style={'width':'100%'}, children=[
        dcc.Dropdown(
            id='preset-dropdown',
            options=[{'label': k, 'value': k} for k in presets],
            placeholder='Selecione uma pré-configuração'
        )
    ]),

    # Tabs de visualização
    dcc.Tabs(id='plot-tabs', value='tab-2d', className="m-0", children=[
        dcc.Tab(label='Séries temporais 2D', value='tab-2d'),
        dcc.Tab(label='Espaço de fase 2D', value='tab-phase'),
        dcc.Tab(label='Superfície 3D', value='tab-3d-surface'),
        dcc.Tab(label='Mapa de Poincaré 3D', value='tab-3d-poincare'),
        dcc.Tab(label='Tubo espaço de fase 3D', value='tab-3d-tube'),
        dcc.Tab(label='Diagrama de bifurcação', value='tab-bifurcation'),
        dcc.Tab(label='Gráfico de recorrência', value='tab-recurrence'),
    ]),

    # Gráfico
    html.Div(
        dcc.Loading(
            dcc.Graph(id='duffing-graph', config={'responsive': True}, style={'width': '100%', 'height': '70vh'}),
            type='circle',
            style={'width': '100%', 'height': '100%'}
        ),
        style={'width': '100%', 'height': '70vh'}
    ),

    # Descrição
    html.Div(id='description-text', className="p-3 fst-italic bg-white border-top border-bottom"),

    # Sliders e Inputs
    html.Div(className="p-3 bg-white", style={'width': '100%'}, children=[
        *[
            html.Div(className="mb-3", children=[
                html.Label(label, className="form-label"),
                dcc.Slider(id=param, min=mn, max=mx, step=stp, value=defaults[param]),
                dcc.Input(id=f"{param}-input", type='number', value=defaults[param], className='form-control mt-1')
            ]) for param, label, mn, mx, stp in [
                ('delta', 'δ (amortecimento)', 0, 1, 0.05),
                ('alpha', 'α (rigidez linear)', -2, 2, 0.1),
                ('beta', 'β (não-linear)', -2, 2, 0.1),
                ('A', 'A (amplitude)', 0, 2, 0.05),
                ('phi', 'ϕ (frequência)', 0.4, 5, 0.1),
                ('epsilon', 'ε (sensibilidade)', 0, 1, 0.05)
            ]
        ]
    ]),
])

# --- Callbacks ---

# Redirecionamento após timer
@app.callback(
    Output("url", "pathname"),
    Input("splash-timer", "n_intervals"),
    Input("url", "pathname")  # Adiciona o pathname atual como entrada
)
def redirect_after_timer(n, current_pathname):
    if n >= 1 and current_pathname != "/app":
        return "/app"
    return no_update

# Roteador de páginas 
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/app":
        return app_page
    return index_page
    return no_update

# Callbacks combinados para atualizar os inputs (delta, alpha, beta, A, phi, epsilon)
for param in ['delta', 'alpha', 'beta', 'A', 'phi', 'epsilon']:
    @app.callback(
        Output(f'{param}-input', 'value'),
        [Input(param, 'value'),          # Valor do slider
         Input('preset-dropdown', 'value')]  # Valor do dropdown de presets
    )
    def update_input(slider_value, preset, param=param):
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == param:  # Se foi o slider
            return slider_value
        elif trigger_id == 'preset-dropdown' and preset in presets:
            return presets[preset][param]
        return no_update

# Callbacks para atualizar os sliders a partir dos inputs
for param in ['delta', 'alpha', 'beta', 'A', 'phi', 'epsilon']:
    @app.callback(
        Output(param, 'value'),
        Input(f'{param}-input', 'value')
    )
    def update_slider(input_value):
        return input_value

# Callback para atualizar o gráfico e a descrição
@app.callback(
    [Output('duffing-graph', 'figure'), Output('description-text', 'children')],
    [Input(f'{p}-input', 'value') for p in ['delta', 'alpha', 'beta', 'A', 'phi', 'epsilon']] +
    [Input('plot-tabs', 'value')]
)
def update_graph(delta, alpha, beta, A, phi, epsilon, tab):
    layout = dict(template='plotly_white', margin=dict(l=40, r=40, t=50, b=40))

    if tab == 'tab-2d':
        fig = go.Figure()
        for x0, v0, clr, lbl in [
            (1, 2, 'blue', 'ε=0'),
            (1 + epsilon, 2 + epsilon, 'green', f'ε=+{epsilon:.2f}'),
            (1 - epsilon, 2 - epsilon, 'red', f'ε=-{epsilon:.2f}')
        ]:
            t, x, v = solve_base(delta, alpha, beta, A, phi, x0, v0)
            fig.add_trace(go.Scatter(x=t, y=x, mode='lines', name=f"x(t) {lbl}", line=dict(color=clr)))
            fig.add_trace(go.Scatter(x=t, y=v, mode='lines', name=f"x'(t) {lbl}", line=dict(color=clr, dash='dot')))
        fig.update_layout(title="", xaxis_title="t", yaxis_title="x, x'", **layout)
        desc = ("Aqui comparamos a posição x(t) e velocidade x'(t) para três condições iniciais "
                "levemente distintas, mostrando como pequenas variações em ε geram trajetórias divergentes—"
                "essência da sensibilidade às condições iniciais.")
    elif tab == 'tab-phase':
        fig = go.Figure()
        # 1) Trajetórias para cada ε
        for x0, v0, clr, lbl in [
            (1, 2, 'blue',  'ε=0'),
            (1+epsilon, 2+epsilon, 'green', f'ε=+{epsilon:.2f}'),
            (1-epsilon, 2-epsilon, 'red',   f'ε=-{epsilon:.2f}')
        ]:
            _, x, v = solve_base(delta, alpha, beta, A, phi, x0, v0)
            fig.add_trace(go.Scatter(
                x=x, y=v, mode='lines', name=f"Trajetória {lbl}",
                line=dict(color=clr)
            ))

        # 2) Malha para o campo de direção
        X_vals = np.linspace(-2, 2, 20)
        V_vals = np.linspace(-2, 2, 20)
        X, V = np.meshgrid(X_vals, V_vals)

        # Calcula derivadas no grid
        DX = V
        DV = -delta * V - alpha * X - beta * X**3 + A * np.cos(phi * 0)  # t=0 para direção geral

        # Normaliza vetores para visualização
        M = np.hypot(DX, DV)
        DXn = DX / M
        DVn = DV / M

        # Adiciona cada seta como segmento de reta
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                x_start = X[i, j]
                y_start = V[i, j]
                x_end   = x_start + 0.2 * DXn[i, j]
                y_end   = y_start + 0.2 * DVn[i, j]
                fig.add_trace(go.Scatter(
                    x=[x_start, x_end], y=[y_start, y_end],
                    mode='lines',
                    line=dict(color='gray', width=1),
                    showlegend=False
                ))

        fig.update_layout(
            title="", 
            xaxis_title="x", 
            yaxis_title="x'",
            template='plotly_white',
            margin=dict(l=40, r=40, t=50, b=40)
        )
        desc = (
            "Retrato de fase mostrando (x, x') para diferentes ε, com o campo de "
            "direção sobreposto (setas cinza) indicando o fluxo instantâneo do sistema."
        )

    elif tab == 'tab-3d-surface':
        P, B = np.meshgrid(np.linspace(0.1, 5, 30), np.linspace(-2, 2, 30))
        Amp = np.zeros_like(P)
        for i in range(P.shape[0]):
            for j in range(P.shape[1]):
                t, x, _ = solve_base(delta, alpha, B[i, j], A, P[i, j])
                Amp[i, j] = np.max(np.abs(x[-200:]))
        fig = go.Figure(go.Surface(x=P, y=B, z=Amp, colorscale='Viridis'))
        fig.update_layout(title="",
                          scene=dict(xaxis_title="ϕ", yaxis_title="β", zaxis_title="Amplitude"), **layout)
        desc = ("Superfície 3D que mapeia a amplitude estacionária de x em função da frequência "
                "ϕ e do termo não-linear β. Picos indicam regiões de ressonância ou instabilidade.")
    elif tab == 'tab-3d-poincare':
        if phi == 0:
            # impossible to compute Poincaré when phi=0
            fig = go.Figure()
            fig.update_layout(
                title="Mapa de Poincaré 3D",
                template='plotly_white',
                annotations=[dict(
                    text="ϕ = 0 → sem forçamento periódico; Poincaré não disponível.",
                    xref="paper", yref="paper", showarrow=False,
                    x=0.5, y=0.5, font=dict(size=16, color="red")
                )]
            )
            desc = "Mapeamento de Poincaré indisponível quando ϕ = 0."
        else:
            period = 2 * np.pi / phi
            pts = np.arange(1, int(defaults['t_end'] / period)) * period
            solp = solve_ivp(
                duffing, [pts[0], pts[-1]], [1, 0],
                t_eval=pts,
                args=(delta, alpha, beta, A, phi)
            )
            fig = go.Figure(go.Scatter3d(
                x=solp.y[0], y=solp.y[1], z=pts,
                mode='markers', marker=dict(size=4)
            ))
            fig.update_layout(
                title="Mapa de Poincaré 3D",
                scene=dict(xaxis_title="x", yaxis_title="x'", zaxis_title="Tempo"),
                template='plotly_white'
            )
            desc = ("Mapa de Poincaré mostrando (x, x') a cada período do forçamento.")
    elif tab == 'tab-3d-tube':
        t, x, v = solve_base(delta, alpha, beta, A, phi)
        fig = go.Figure(go.Scatter3d(x=x, y=v, z=t, mode='lines', line=dict(width=2)))
        fig.update_layout(title="",
                          scene=dict(xaxis_title="x", yaxis_title="x'", zaxis_title="Tempo"), **layout)
        desc = ("Trajetória contínua (x, x', t) formando um tubo no espaço tridimensional. "
                "Revela a evolução temporal como uma hélice no espaço de fase.")
    # -- 12) Recurrence Plot --
    elif tab == 'tab-recurrence':
        # Reconstrói (x, x') e calcula matriz de recorrência
        t, x, v = solve_base(delta, alpha, beta, A, phi)
        data = np.vstack([x, v]).T
        # distância par-a-par
        D = np.linalg.norm(data[:, None, :] - data[None, :, :], axis=2)
        # limiar = 10% do máximo
        eps = 0.1 * np.nanmax(D)
        R = (D < eps).astype(int)

        fig = go.Figure(go.Heatmap(
            z=R,
            showscale=False,
            colorscale=[[0, 'white'], [1, 'black']]
        ))
        fig.update_layout(
            title="Gráfico de recorrência",
            xaxis_title="Índice de Tempo",
            yaxis_title="Índice de Tempo",
            template='plotly_white',
            margin=dict(l=40, r=40, t=50, b=40)
        )
        desc = "Plot binário de recorrências: diagonais longas indicam periodicidade; manchas, caos."
    else:
        if phi == 0:
            fig = go.Figure()
            fig.update_layout(
                title="Diagrama de Bifurcação",
                template='plotly_white',
                annotations=[dict(
                    text="ϕ = 0 → sem forçamento periódico; Bifurcação não disponível.",
                    xref="paper", yref="paper", showarrow=False,
                    x=0.5, y=0.5, font=dict(size=16, color="red")
                )]
            )
            desc = "Diagrama de bifurcação indisponível quando ϕ = 0."
        else:
            A_vals, xp, Ap = np.linspace(0, 2, 300), [], []
            period = 2 * np.pi / phi
            for Ai in A_vals:
                pts = np.arange(1, int(defaults['t_end'] / period)) * period
                solb = solve_ivp(
                    duffing, [pts[0], pts[-1]], [1, 0],
                    t_eval=pts,
                    args=(delta, alpha, beta, Ai, phi)
                )
                xp.extend(solb.y[0])
                Ap.extend([Ai] * len(solb.y[0]))
            fig = go.Figure(go.Scatter(x=Ap, y=xp, mode='markers', marker=dict(size=2)))
            fig.update_layout(
                title="Diagrama de Bifurcação",
                xaxis_title="A", yaxis_title="x (Poincaré)",
                template='plotly_white'
            )
            desc = ("Diagrama de bifurcação plotando x no Mapa de Poincaré conforme A varia.")

    return fig, desc

# --- Execução ---

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
