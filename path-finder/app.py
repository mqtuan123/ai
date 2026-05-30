





from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

import json

from astar import find_shortest_path

app = Flask(__name__)

with open(
    "data/data.json",
    "r",
    encoding="utf-8"
) as f:

    graph_data = json.load(f)

GRAPH = graph_data["nodes"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/nodes")
def get_nodes():

    nodes = []

    for node_id, node in GRAPH.items():

        nodes.append({
            "id": node_id,
            "lat": node["lat"],
            "lng": node["lng"]
        })

    return jsonify(nodes)


@app.route("/api/find-path", methods=["POST"])
def find_path():

    data = request.get_json()

    start = data["start"]
    end = data["end"]

    path_ids = find_shortest_path(
        GRAPH,
        start,
        end
    )

    coordinates = []

    for node_id in path_ids:

        node = GRAPH[node_id]

        coordinates.append({
            "id": node_id,
            "lat": node["lat"],
            "lng": node["lng"]
        })

    return jsonify({
        "path": coordinates
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5005,
        debug=True
    )