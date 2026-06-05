from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import math
import os
from utils.astar import a_star_algorithm

app = Flask(__name__, template_folder='templates')
CORS(app)

with open('data/map_data.json', 'r', encoding='utf-8') as f:
    MAP_DATA = json.load(f)

def find_closest_node(click_coords, nodes):
    cx, cy = click_coords
    closest_node = None
    min_dist = float('inf')
    
    for node_id, coords in nodes.items():
        dist = math.sqrt((cx - coords['x'])**2 + (cy - coords['y'])**2)
        if dist < min_dist:
            min_dist = dist
            closest_node = node_id
            
    return closest_node

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def get_image(filename):
    return send_from_directory(os.getcwd(), filename)

@app.route('/api/find-path', methods=['POST'])
def find_path():
    data = request.json
    start_point = data['start'] 
    end_point = data['end']     
    
    closest_start_node = find_closest_node((start_point['x'], start_point['y']), MAP_DATA['nodes'])
    closest_end_node = find_closest_node((end_point['x'], end_point['y']), MAP_DATA['nodes'])
    
    # In ra terminal để debug xem bắt đúng node gần chấm đỏ/xanh chưa
    print(f"-> Điểm bắt đầu click gần Node: {closest_start_node}")
    print(f"-> Điểm kết thúc click gần Node: {closest_end_node}")
    
    path_nodes = a_star_algorithm(MAP_DATA, closest_start_node, closest_end_node)
    
    if not path_nodes:
        return jsonify({"status": "error", "message": "Không tìm thấy đường đi giữa các node cố định"}), 404
        
    result_path = []
    result_path.append({"x": start_point['x'], "y": start_point['y']})
    for node_id in path_nodes:
        result_path.append({
            "x": MAP_DATA['nodes'][node_id]['x'],
            "y": MAP_DATA['nodes'][node_id]['y']
        })
    result_path.append({"x": end_point['x'], "y": end_point['y']})
        
    return jsonify({
        "status": "success",
        "path": result_path
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)