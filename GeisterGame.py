# coding:utf-8

# マジックナンバーは使いたくないよね(随時追加)
WidthOfBoard = 6  # ボードの幅
HeightOfBoard = 6  # 高さ
MaxNumOfGhost = 8  # プレイヤーの持ち駒の数

MyselfPlayer = 0  # 1番目のプレイヤ(1人称で見た際に自分として扱う)
OpponentPlayer = 1  # 2番目のプレイヤ(敵として扱う)
NobodyPlayer = -1  # MyselfPlayerでもOpponentPlayerでもない場合に使う値(エラー値)

"""駒の色を推定/判定する際に用いる"""
ColorRed = -1.0  # 赤確定
ColorBlue = 1.0  # 青確定
ColorUncertain = 0.0  # 完全に不明


class Game:
    def __init__(self):
        super().__init__()


class GameState:
    def __init__(self):
        super().__init__()


def main():
    print("Hello World")


if __name__ == "__main__":
    main()
