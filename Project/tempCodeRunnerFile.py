def min_consistent_ac3(grid):
    """
    Xây dựng danh sách các nước đi hợp lệ từ mỗi ô trong mê cung.
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Các hướng di chuyển: lên, xuống, trái, phải

    possible_moves = {(r, c): [] for r in range(rows) for c in range(cols) if grid[r][c] != 1}

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:  # Không phải tường
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
                        possible_moves[(r, c)].append((nr, nc))

    queue = list(possible_moves.keys())
    while queue:
        current = queue.pop(0)
        updated = False
        neighbors = possible_moves[current]

        if not neighbors:
            del possible_moves[current]
            updated = True

        for neighbor in neighbors:
            if neighbor in possible_moves and current not in possible_moves[neighbor]:
                possible_moves[neighbor].remove(current)
                updated = True

            if updated:
                queue.append(neighbor)

    return possible_moves

def enhanced_heuristic(a, b, grid):
    """
    Heuristic tính khoảng cách Manhattan và cộng thêm chi phí phạt nếu gần tường.
    """
    manhattan_distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    wall_penalty = 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = a[0] + dr, a[1] + dc
        if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])) or grid[nr][nc] == 1:
            wall_penalty += 1

    return manhattan_distance + wall_penalty * 5  # Phạt 5 điểm cho mỗi tường gần

'''def heuristic(a, b):
    """
    Tính toán khoảng cách Manhattan giữa hai ô.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])'''


def backtrack_with_ac3(grid, ghost_position, pacman_position, max_depth=600):
    possible_moves = min_consistent_ac3(grid)

    def search(path, depth, visited):
        if depth > max_depth:  # Giới hạn độ sâu
            return None
        current = path[-1]
        if current == pacman_position:  # Đạt được Pacman
            return path

        # Đánh dấu ô hiện tại là đã thăm
        visited[current] = visited.get(current, 0) + 1
        if visited[current] > 3:  # Giới hạn số lần quay lại một ô
            return None

        # Sử dụng hàng đợi ưu tiên để tìm nước đi tốt nhất dựa trên heuristic
        pq = []
        for next_pos in possible_moves.get(current, []):
            if visited.get(next_pos, 0) < 2:  # Chỉ thử các nước đi ít bị thăm
                priority = enhanced_heuristic(next_pos, pacman_position, grid)
                heapq.heappush(pq, (priority, next_pos))

        while pq:
            _, next_pos = heapq.heappop(pq)
            result = search(path + [next_pos], depth + 1, visited)
            if result:
                return result

        # Nếu không có nước đi ưu tiên, thử các nước đi ít bị thăm
        for next_pos in possible_moves.get(current, []):
            if visited.get(next_pos, 0) < 2:
                result = search(path + [next_pos], depth + 1, visited)
                if result:
                    return result

        # Nếu không tìm được đường đi, xóa ô hiện tại khỏi tập `visited`
        visited[current] -= 1
        if visited[current] <= 0:
            del visited[current]

        return None

    # Khởi tạo tìm kiếm với từ điển `visited`
    return search([ghost_position], 0, {})


