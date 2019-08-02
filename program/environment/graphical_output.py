
import plotly.graph_objects as go


def plot_static(all_edges_x, all_edges_y, all_nodes_x, all_nodes_y):
	edge_trace = go.Scatter(
    x=all_edges_x, y=all_edges_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

	node_trace = go.Scatter(
    x=all_nodes_x, y=all_nodes_y,
    mode='markers',
    hovertext=["Text A", "Text B", "Text C", "Text D", "Text E"],
    hoverinfo="text",
    marker=dict(
        color="green"
    ))

	fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>BWKI KIndsköpfe - Autonomes Straßennetz',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
	fig.show()

