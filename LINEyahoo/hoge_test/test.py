class Circle:
    def __init__(self, radius):
        # インスタンス変数に値を代入
        self.radius = radius

    # 関数を定義
    def area(self):
        return radius * radius * 3.14


radius = 10
# インスタンスの生成
circle = Circle(radius)

print("円の半径:", radius)
print("円の面積:", circle.area())
