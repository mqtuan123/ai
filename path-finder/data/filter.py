import json

def is_in_hust(lat, lng):
    # Tọa độ khung giới hạn (bounding box) xấp xỉ của Bách khoa Hà Nội
    min_lat, max_lat = 21.0016, 21.0076
    min_lng, max_lng = 105.8412, 105.8475
    
    return min_lat <= lat <= max_lat and min_lng <= lng <= max_lng

# Đọc dữ liệu từ file data.json của bạn
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

nodes = data.get('nodes', {})
filtered_nodes = {}

# Lọc các node nằm trong khuôn viên trường
for node_id, node_info in nodes.items():
    if is_in_hust(node_info['lat'], node_info['lng']):
        filtered_nodes[node_id] = node_info

# Loại bỏ các node lân cận (neighbors) đã bị xóa khỏi danh sách
for node_id, node_info in filtered_nodes.items():
    original_neighbors = node_info.get('neighbors', [])
    valid_neighbors = [n for n in original_neighbors if n in filtered_nodes]
    filtered_nodes[node_id]['neighbors'] = valid_neighbors

# Lưu kết quả ra file JSON mới
output_data = {"nodes": filtered_nodes}

with open('hust_nodes.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=4, ensure_ascii=False)

print(f"Hoàn tất! Đã giữ lại {len(filtered_nodes)} nodes nằm trong Đại học Bách khoa Hà Nội.")