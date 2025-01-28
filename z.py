def main(lines):
    # 1行目：盤面サイズ
    n = int(lines[0])
    
    # 2行目：操作回数
    q = int(lines[1])
    
    # 面の初期化（すべて白）
    grid = [['.'] * n for _ in range(n)]
    
    # 操作情報の読み込みと処理
    for i in range(q):
        x, y, z = map(int, lines[2 + i].split())
        
        # 中心座標（0-indexed）
        cx, cy = x - 1, y - 1
        
        # 縦方向の塗りつぶし
        for j in range(-z, z + 1):
            if 0 <= cx + j < n:
                grid[cx + j][cy] = '#'
        
        # 横方向の塗りつぶし
        for j in range(-z, z + 1):
            if 0 <= cy + j < n:
                grid[cx][cy + j] = '#'
    
    # 結果の出力
    sys.stdout.write("\n".join("".join(row) for row in grid) + "\n"