import graph_tool.all as gt
print("Generating graph...")

g = gt.price_network(1000)
pos = gt.sfdp_layout(g)
gt.graph_draw(g, pos=pos, output="graph1.pdf")