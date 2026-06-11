import heapq
import math

def heuristic(node_coords, target_coords):
    # Dùng Euclid tính khoảng cách
    return math.sqrt((node_coords['x'] - target_coords['x'])**2 + (node_coords['y'] - target_coords['y'])**2)

def a_star_algorithm(graph, start_node, end_node):
    nodes = graph['nodes']
    
    # 1. Khởi tạo danh sách kề vô hướng từ dữ liệu edges
    adj_list = {node_id: [] for node_id in nodes}
    for edge in graph['edges']:
        u, v, w = edge['from'], edge['to'], edge['weight']
        if u in adj_list and v in adj_list:
            adj_list[u].append((v, w))
            adj_list[v].append((u, w))

    # 2. Hàng đợi ưu tiên lưu cấu trúc: (f_score, current_node)
    open_set = []
    heapq.heappush(open_set, (0.0, start_node))
    
    parent = {}
    g_score = {node_id: float('inf') for node_id in nodes}
    g_score[start_node] = 0.0
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        # Nếu đã chạm tới đích, tiến hành truy vết ngược đường đi
        if current == end_node:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start_node)
            path.reverse()
            return path
            
        for neighbor, weight in adj_list[current]:
            tentative_g_score = g_score[current] + weight
            
            if tentative_g_score < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(nodes[neighbor], nodes[end_node])
                
                # Kiểm tra tránh đẩy trùng node vào open_set
                if not any(item[1] == neighbor for item in open_set):
                    heapq.heappush(open_set, (f_score, neighbor))
                    
    return None