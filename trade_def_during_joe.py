import plotly.graph_objects as go

data = [
    {'Source': 'Canada Exports 2024', 'Target': ' ', 'Value': 349359.90, 'type': 'export'},
    {'Source': ' ', 'Target': 'USA Imports 2024', 'Value': 412695.70, 'type': 'import'},
    {'Source': 'Canada Exports 2023', 'Target': ' ', 'Value': 354356.00, 'type': 'export'},
    {'Source': ' ', 'Target': 'USA Imports 2023', 'Value': 418618.70, 'type': 'import'},
    {'Source': 'Canada Exports 2022', 'Target': ' ', 'Value': 359236.50, 'type': 'export'},
    {'Source': ' ', 'Target': 'USA Imports 2022', 'Value': 437429.10, 'type': 'import'},
    {'Source': 'Canada Exports 2021', 'Target': ' ', 'Value': 309604.00, 'type': 'export'},
    {'Source': ' ', 'Target': 'USA Imports 2021', 'Value': 357274.70, 'type': 'import'}
]

labels = ['Canada Exports 2024', 'Canada Exports 2023', 'Canada Exports 2022', 'Canada Exports 2021', ' ', 'USA Imports 2024', 'USA Imports 2023', 'USA Imports 2022', 'USA Imports 2021']
source_indices = [labels.index(d['Source']) for d in data]
target_indices = [labels.index(d['Target']) for d in data]
values = [d['Value'] for d in data]
link_colors = ['rgba(0,255,0,0.2)' if d['type'] == 'export' else 'rgba(255,0,0,0.2)' for d in data] 


node_x = [0, 0, 0, 0, 0.5, 1, 1, 1, 1]
node_y = [0.1, 0.3, 0.5, 0.7, 0.5, 0.1, 0.3, 0.5, 0.7]


fig = go.Figure(data=[go.Sankey(
    node=dict(
      pad=25,
      thickness=10,
      line=dict(color="black", width=0.5),
      label=labels,
      x=node_x,
      y=node_y
    ),
    link=dict(
      arrowlen=15,
      source=source_indices,
      target=target_indices,
      value=values,
      color=link_colors
  ))])


fig.add_annotation(
    x=0.5,  
    y=0.06, 
    text="250(B)+ Total Deficit",
    showarrow=False,  
    font=dict(size=14, color="red"),
    bgcolor="rgba(255,255,255,0.8)",  
    xanchor="center"
)


fig.update_layout(
    title_text="USA-Canada  Balance of Trade (Prev Gov's Tenure)",
    font_size=10,
)
fig.show()
