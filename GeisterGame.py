# coding:utf-8

# マジックナンバーは使いたくないよね(随時追加)
WidthOfBoard = 6  # ボードの幅
HeightOfBoard = 6  # 高さ
MaxNumOfGhost = 8  # プレイヤーの持ち駒の数

MyselfPlayer = 0  # 1番目のプレイヤ(1人称で見た際に自分として扱う)
OpponentPlayer = 1  # 2番目のプレイヤ(敵として扱う)
NobodyPlayer = -1  # MyselfPlayerでもOpponentPlayerでもない場合に使う値(エラー値)(デフォルト値)

"""駒の色を推定/判定する際に用いる"""
ColorUncertain = 0.0  # 完全に不明(デフォルト値)
ColorRed = -1.0  # 赤確定
ColorBlue = 1.0  # 青確定

# 駒にIDくっつけてボードではIDで管理が現実的かなぁ
class Piece:
    """駒の情報を保管"""
    def __init__(self, x: int, y: int, color: float):
        self.x = x  # x座標
        self.y = y  # y座標
        self.color = color  # 駒の色
        self.estimated_color = ColorUncertain  #駒の色に対する推定値(駒推定の時に使うはず)
        
    

class Board:
    """ガイスターの盤面を管理するクラス"""

    def __init__(self):
        self.all_board = hoge

# プレイヤの選択肢を表現する際にプレイヤクラスは必須では？なんならボードがいらない説が出てきた
class Player:
    """プレイヤを管理するクラス"""
    def

class Move:
    """プレイヤのとり得る手を管理するクラス"""

class Game:
    """ゲーム全体を管理"""

    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]  # プレイに参加する2人のプレイヤを保存
        self.turn_player = NobodyPlayer  # 現在のターンプレイヤを保存
        self.first_turn_player = NobodyPlayer  # 先手のプレイヤを保存
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
