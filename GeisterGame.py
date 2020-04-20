# coding:utf-8

# マジックナンバーは使いたくないよね(随時追加)
WidthOfBoard = 6  # ボードの幅
HeightOfBoard = 6  # 高さ
MaxNumOfGhost = 8  # プレイヤーの持ち駒の数

MyselfPlayer = 0  # 1番目のプレイヤ(1人称で見た際に自分として扱う)(デフォルト値)
OpponentPlayer = 1  # 2番目のプレイヤ(敵として扱う)
NobodyPlayer = -1  # MyselfPlayerでもOpponentPlayerでもない場合に使う値(エラー値)

"""駒の色を推定/判定する際に用いる"""
ColorRed = -1.0  # 赤確定
ColorBlue = 1.0  # 青確定
ColorUncertain = 0.0  # 完全に不明

# 駒にIDくっつけてボードではIDで管理が現実的かなぁ
class Piece:
    hoge

class Board:
    """ガイスターの盤面を管理するクラス"""

    def __init__(self):
        self.all_board = 


class Game:
    """ゲーム全体を管理"""

    def __init__(self):
        self.players = []  # プレイに参加する2人のプレイヤを保存
        self.turn_player = MyselfPlayer  # 後手のプレイヤを保存
        self.first_turn_player = MyselfPlayer  # 先手のプレイヤを保存
        self.board = Board()  # 盤面(ボードの状態)を保存
        self.move_num = 0  # 何手目かを保存


class GameState:
    def __init__(self):
        super().__init__()

    def game_is_over() -> bool:
        """ゲームの終了を判定"""


def main():
    print("Hello World")


if __name__ == "__main__":
    main()
