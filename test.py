import plotly.graph_objects as go
import numpy as np

def graficar_circulo_mohr(sigma_x, sigma_y, tau_xy):
    sigma_prom = (sigma_x + sigma_y) / 2
    radio = np.sqrt(((sigma_x - sigma_y) / 2) ** 2 + tau_xy ** 2)

    theta = np.linspace(0, 2 * np.pi, 100)
    sigma = sigma_prom + radio * np.cos(theta)
    tau = radio * np.sin(theta)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sigma, y=tau, mode='lines', name='Círculo de Mohr'))
    fig.add_trace(go.Scatter(x=[sigma_prom], y=[0], mode='markers', marker=dict(color='red'), name='Centro'))
    fig.add_trace(go.Scatter(x=[sigma_x, sigma_y], y=[tau_xy, -tau_xy], mode='markers', marker=dict(color='green'), name='Puntos de tensión'))
    fig.update_layout(
        title='Círculo de Mohr',
        xaxis_title='Tensión Normal (σ)',
        yaxis_title='Tensión Cortante (τ)',
        xaxis=dict(scaleanchor="y", scaleratio=1),
        yaxis=dict(scaleanchor="x", scaleratio=1),
        xaxis_zeroline=True,
        yaxis_zeroline=True,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

def graficar_circulo_mohr_3d(sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx):
    # Tensor de tensiones
    T = np.array([
        [sigma_x, tau_xy, tau_zx],
        [tau_xy, sigma_y, tau_yz],
        [tau_zx, tau_yz, sigma_z]
    ])
    # Tensiones principales (autovalores de T)
    tensiones_principales = np.linalg.eigvalsh(T)
    sigma_1, sigma_2, sigma_3 = sorted(tensiones_principales, reverse=True)

    # Círculos
    centros = [(sigma_1 + sigma_2) / 2, (sigma_2 + sigma_3) / 2, (sigma_3 + sigma_1) / 2]
    radios = [np.abs(sigma_1 - sigma_2) / 2, np.abs(sigma_2 - sigma_3) / 2, np.abs(sigma_3 - sigma_1) / 2]

    fig = go.Figure()
    theta = np.linspace(0, 2 * np.pi, 100)
    for centro, radio in zip(centros, radios):
        sigma = centro + radio * np.cos(theta)
        tau = radio * np.sin(theta)
        fig.add_trace(go.Scatter3d(x=sigma, y=tau, z=np.zeros_like(sigma), mode='lines'))

    fig.update_layout(
        title='Círculo de Mohr en 3D',
        scene=dict(
            xaxis_title='Tensión Normal (σ)',
            yaxis_title='Tensión Cortante (τ)',
            zaxis_title='Tensión Cortante (τ)',
            aspectratio=dict(x=1, y=1, z=1)
        )
    )
    return fig

def graficar_circulo_mohr_3d_esferas(sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx):
    """
    Grafica el círculo de Mohr en 3D usando Plotly.

    Args:
        sigma_x: Tensión normal en el eje x.
        sigma_y: Tensión normal en el eje y.
        sigma_z: Tensión normal en el eje z.
        tau_xy: Tensión cortante en el plano xy.
        tau_yz: Tensión cortante en el plano yz.
        tau_zx: Tensión cortante en el plano zx.
    """

    # Tensiones principales
    sigma_1 = (sigma_x + sigma_y) / 2 + np.sqrt(((sigma_x - sigma_y) / 2)**2 + tau_xy**2)
    sigma_2 = (sigma_x + sigma_y) / 2 - np.sqrt(((sigma_x - sigma_y) / 2)**2 + tau_xy**2)
    sigma_3 = sigma_z

    # Centros y radios de los círculos
    centros = [(sigma_1 + sigma_2) / 2, (sigma_2 + sigma_3) / 2, (sigma_3 + sigma_1) / 2]
    radios = [np.abs(sigma_1 - sigma_2) / 2, np.abs(sigma_2 - sigma_3) / 2, np.abs(sigma_3 - sigma_1) / 2]

    # Crear la figura
    fig = go.Figure()

    # Generar puntos para las esferas
    phi = np.linspace(0, np.pi, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    phi, theta = np.meshgrid(phi, theta)

    for centro, radio in zip(centros, radios):
        x = centro + radio * np.sin(phi) * np.cos(theta)
        y = radio * np.sin(phi) * np.sin(theta)
        z = radio * np.cos(phi)
        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.5, name=f'Esfera con centro en {centro}'))

    # Configurar el diseño
    fig.update_layout(
        title='Círculo de Mohr en 3D',
        scene=dict(
            xaxis_title='Tensión Normal (σ)',
            yaxis_title='Tensión Cortante (τ)',
            zaxis_title='Tensión Cortante (τ)',
            aspectratio=dict(x=1, y=1, z=1)
        )
    )
    return fig

# Ejemplo de uso
# graficar_circulo_mohr(20, -10, 15)
# graficar_circulo_mohr_3d(100, 50, 30, 25, 15, 10)
# graficar_circulo_mohr_3d_esferas(100, 50, 30, 25, 15, 10)
