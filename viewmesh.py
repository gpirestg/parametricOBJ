import streamlit as st
import plotly.graph_objects as go
import trimesh
import os

st.title("3D OBJ Viewer")

# === UI Controls ===
reload_mesh = st.button("🔄 Reload Mesh")
show_wireframe = st.checkbox("Show Wireframe", value=True)

# === Load mesh (reload on demand) ===
@st.cache_data(show_spinner=False)
def load_mesh():
    return trimesh.load("model.obj")

# Force reload if button is clicked
if reload_mesh:
    # Remove from cache so it reloads
    load_mesh.clear()

# Load mesh (fresh or cached)
mesh = load_mesh()

# Extract mesh data
x, y, z = mesh.vertices.T
i, j, k = mesh.faces.T

# Create surface mesh
surface = go.Mesh3d(
    x=x, y=y, z=z,
    i=i, j=j, k=k,
    opacity=1,
    color='red',
    flatshading=True
)
surface.lighting = dict(ambient=0.5, diffuse=0.5, fresnel=0.1, specular=0.5, roughness=0.5)
surface.lightposition = dict(x=100, y=200, z=0)

# Add wireframe edges
fig_data = [surface]
if show_wireframe:
    for face in mesh.faces:
        for edge in [(0, 1), (1, 2), (2, 0)]:
            x0, y0, z0 = mesh.vertices[face[edge[0]]]
            x1, y1, z1 = mesh.vertices[face[edge[1]]]
            fig_data.append(go.Scatter3d(
                x=[x0, x1, None],
                y=[y0, y1, None],
                z=[z0, z1, None],
                mode='lines',
                line=dict(color='black', width=2),
                showlegend=False,
                hoverinfo='skip'
            ))

# Build and display figure
fig = go.Figure(data=fig_data)
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode='data',
        bgcolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig, use_container_width=True)
