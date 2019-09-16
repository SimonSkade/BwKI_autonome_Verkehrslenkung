
#import plotly.graph_objects as go



def convert_to_hex(color_red):

    color_green = 255-color_red
    color_blue = 0
    return '#%02x%02x%02x' % (color_red, color_green, color_blue)

# def plot_static_plotly(all_edges_x, all_edges_y, all_nodes_x, all_nodes_y, vertexes, edges):
#     edge_trace = go.Scatter(
#     x=all_edges_x, y=all_edges_y,
#     line=dict(width=0.5, color='#888', shape="spline"),
#     hovertext=["Gewicht: " + str(x.weight) for x in edges],
#     hoverinfo='text',
#     mode='lines')

#     node_trace = go.Scatter(
#     x=all_nodes_x, y=all_nodes_y,
#     mode='markers',
#     hovertext=["Knoten " + str(x.ID) + "\n" + "--> " + str(x.connections) for x in vertexes],
#     hoverinfo="text",
#     marker=dict(
#         color="green"
#     ))



#     fig = go.Figure(data=[edge_trace, node_trace],
#         layout=go.Layout(
#             title='<br>BWKI KIndsköpfe - Autonomes Straßennetz',
#             titlefont_size=16,
#             showlegend=False,
#             hovermode='closest',
#             margin=dict(b=20,l=5,r=5,t=40),
#             annotations=[ dict(
#                 text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
#                 showarrow=False,
#                 xref="paper", yref="paper",
#                 x=0.005, y=-0.002 ) ],
#             xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#             yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
#             )
#     fig.show()

import networkx as nx
def convert_to_networkx(nodes, edges):
    G = nx.DiGraph()
    G.add_weighted_edges_from([(x.v1_id,x.v2_id,x.weight) for x in edges])
    return G

import matplotlib.pyplot as plt
def plot_from_networkx(nodes, edges):
    G = convert_to_networkx(nodes, edges)

    color = []
    #Finde das kleinste und größte Gewicht
    hoch = edges[0].weight
    tief = edges[0].weight
    for x in edges:
        if hoch < x.weight:
            hoch = x.weight
        elif tief > x.weight:
            tief = x.weight

    
    for x in edges:
        percent = (x.weight - tief) / (hoch - tief) 
        color_red = int(255 * percent)
        color.append(convert_to_hex(color_red))

    nodemap = {}

    for i,node in enumerate(nodes):
        nodemap[i] = node.position
    nx.draw(G, pos=nodemap, with_labels=True,edge_color=color)
    plt.show()



def convert_to_hex_blue(color_blue):
    color_green = 255-color_blue
    color_red = 0
    return '#%02x%02x%02x' % (color_red, color_green, color_blue)

    

def plot_networkx_num_cars(nodes, edges):
    G = convert_to_networkx(nodes, edges)

    color = []
    #Finde das kleinste und größte Gewicht
    hoch = edges[0].n_cars
    tief = edges[0].n_cars
    for x in edges:
        if hoch < x.n_cars:
            hoch = x.n_cars
        elif tief > x.n_cars:
            tief = x.n_cars

    
    for x in edges:
        percent = (x.n_cars - tief) / (hoch - tief) 
        color_blue = int(255 * percent)
        color.append(convert_to_hex_blue(color_blue))

    nodemap = {}

    for i,node in enumerate(nodes):
        nodemap[i] = node.position
    nx.draw(G, pos=nodemap, with_labels=True,edge_color=color)
    plt.show()
    

