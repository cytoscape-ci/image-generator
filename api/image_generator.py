from flask_restful import Resource
import graph_tool.all as gt

from flask import send_file


class ImageGenerator(Resource):

    def get(self):
        print("Generating graph...")

        g = gt.price_network(1000)
        pos = gt.sfdp_layout(g)
        gt.graph_draw(g, pos=pos, output="../images/graph1.pdf")

        return {"message": "OK"}
