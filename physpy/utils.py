import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt

# Define physical body
class Body:
    def __init__(self, name = "Body", mass = 0, type = "point", position = np.array([0, 0, 0]), velocity = np.array([0, 0, 0]), acceleration = np.array([0, 0, 0]), force = np.array([0, 0, 0]), charge = 0):
        self.name = name
        self.mass = mass
        self.type = type
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.force = force
        self.charge = charge

        self.position_history = []
        self.velocity_history = []
        self.acceleration_history = []
        self.force_history = []
        self.time_history = []

    def logger(self, time):
        self.position_history.append(self.position)
        self.velocity_history.append(self.velocity)
        self.acceleration_history.append(self.acceleration)
        self.force_history.append(self.force)
        self.time_history.append(time)

class Plotter:
    def __init__(self, bodies=[], n_dimensions=2):
        self.bodies = bodies
        self.n_dimensions = n_dimensions

    def plot_trajectory(self):
        # Animated trajectory with larger markers and time slider
        if not self.bodies:
            return
        # Extract time steps and position histories
        times = self.bodies[0].time_history
        pos_hist = [np.array(body.position_history) for body in self.bodies]
        # Prepare initial data: markers and static trails
        data = []
        if self.n_dimensions == 2:
            # markers
            for idx, body in enumerate(self.bodies):
                data.append(go.Scatter(
                    x=[pos_hist[idx][0,0]], y=[pos_hist[idx][0,1]],
                    mode='markers', marker=dict(size=2),
                    name=body.name
                ))
            # static trails
            for idx, body in enumerate(self.bodies):
                data.append(go.Scatter(
                    x=pos_hist[idx][:,0], y=pos_hist[idx][:,1],
                    mode='lines', line=dict(width=2),
                    name=body.name+' path', showlegend=False
                ))
        else:
            for idx, body in enumerate(self.bodies):
                data.append(go.Scatter3d(
                    x=[pos_hist[idx][0,0]], y=[pos_hist[idx][0,1]], z=[pos_hist[idx][0,2]],
                    mode='markers', marker=dict(size=8),
                    name=body.name
                ))
            for idx, body in enumerate(self.bodies):
                data.append(go.Scatter3d(
                    x=pos_hist[idx][:,0], y=pos_hist[idx][:,1], z=pos_hist[idx][:,2],
                    mode='lines', line=dict(width=2),
                    name=body.name+' path', showlegend=False
                ))
        # Build frames for animation
        frames = []
        for i, t in enumerate(times):
            frame_data = []
            for idx in range(len(self.bodies)):
                if self.n_dimensions == 2:
                    frame_data.append(go.Scatter(
                        x=[pos_hist[idx][i,0]], y=[pos_hist[idx][i,1]],
                        mode='markers', marker=dict(size=12)
                    ))
                else:
                    frame_data.append(go.Scatter3d(
                        x=[pos_hist[idx][i,0]], y=[pos_hist[idx][i,1]], z=[pos_hist[idx][i,2]],
                        mode='markers', marker=dict(size=8)
                    ))
            frames.append(go.Frame(data=frame_data, name=f"{t:.2f}"))
        # Slider and play button configuration
        sliders = [dict(
            steps=[dict(method='animate', label=f"{t:.2f}",
                        args=[[f"{t:.2f}"], dict(mode='immediate', frame=dict(duration=100, redraw=True), transition=dict(duration=0))]) for t in times],
            transition=dict(duration=0), x=0, y=0,
            currentvalue=dict(font=dict(size=12), prefix='Time: ', visible=True, xanchor='center'),
            len=1.0
        )]
        updatemenus = [dict(
            type='buttons', showactive=False, y=1, x=1.1, xanchor='right', yanchor='top',
            pad=dict(t=0, r=10),
            buttons=[dict(label='Play', method='animate',
                          args=[None, dict(frame=dict(duration=100, redraw=True), transition=dict(duration=0), fromcurrent=True, mode='immediate')])]
        )]
        layout = dict(
            width=600, height=600,
            dragmode='pan' if self.n_dimensions==2 else 'orbit',
            xaxis=dict(constrain='domain', title='x') if self.n_dimensions==2 else None,
            yaxis=dict(scaleanchor='x', scaleratio=1, title='y') if self.n_dimensions==2 else None,
            scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z', aspectmode='cube') if self.n_dimensions==3 else None,
            updatemenus=updatemenus, sliders=sliders
        )
        fig = go.Figure(data=data, layout=layout, frames=frames)
        fig.show()

