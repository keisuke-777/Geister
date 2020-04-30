# coding:utf-8

from typing import List, Tuple, Union
import numpy as np
import array

# マジックナンバーは使いたくないよね(随時追加)
WidthOfBoard = 6  # ボードの幅
HeightOfBoard = 6  # 高さ
MaxNumOfGhost = 8  # プレイヤーの持ち駒の数

MyselfPlayer = 0  # 1番目のプレイヤ(1人称で見た際に自分として扱う)
OpponentPlayer = 1  # 2番目のプレイヤ(敵として扱う)
NobodyPlayer = -1  # MyselfPlayerでもOpponentPlayerでもない場合に使う値(エラー値)(デフォルト値)

"""駒の色を推定/判定する際に用いる"""
EstimatedColorUncertain = 0.0  # 完全に不明(デフォルト値)
EstimatedColorRed = -1.0  # 赤確定
EstimatedColorBlue = 1.0  # 青確定

ColorRed = -1
ColorBlue = 1


class Strategy:
    """プレイヤの戦略を決める"""

    def __init__(self):
        self.plan = "test"


# プレイヤの選択肢を表現する際にプレイヤクラスは必須では？なんならボードがいらない説が出てきた→ボードは対称のゲームを分析するのに便利かも
class Player:
    """一人のプレイヤーの状態をすべて記録するクラス"""

    def __init__(self, player_id: int):
        if (player_id != 0) and (player_id != 1):
            print("プレイヤーが明示的に与えられていません")  # プレイヤIDが不正
        else:
            self.player_id = player_id  # プレイヤIDを保存
        # あとで相手の駒のリストも格納できるようにしといた方がいいかも(駒推測に使える)
        self.strategy = Strategy()

        self.alive_red_pieces_num = 0  # 生きている赤駒の数
        self.alive_blue_pieces_num = 0  # 生きている青駒の数
        self.captured_red_pieces_num = 0  # 捕獲された赤駒の数
        self.captured_blue_pieces_num = 0  # 捕獲された青駒の数


class Board:
    """神の視点でガイスターの盤面を管理するクラス"""

    def __init__(self, player1: Player, player2: Player):

        # 6*6マス(ここにコマのIDを格納)
        self.board = np.array(
            [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ]
        )
        self.player1 = player1
        self.player2 = player2

        # 駒のIDに駒の色を紐付ける
        # ここ気が狂うほど場当たり的なので、あとでなんとかする
        self.pieceArr = array.array(
            "i",
            [
                0,
                ColorRed,  # 1
                ColorRed,  # 2
                ColorRed,  # 3
                ColorRed,  # 4
                ColorBlue,  # 5
                ColorBlue,  # 6
                ColorBlue,  # 7
                ColorBlue,  # 8
                0,
                0,
                ColorBlue,  # 11
                ColorBlue,  # 12
                ColorBlue,  # 13
                ColorBlue,  # 14
                ColorRed,  # 15
                ColorRed,  # 16
                ColorRed,  # 17
                ColorRed,  # 18
            ],
        )

    def reset_board(self):
        """ボードをリセット(IDの初期配置をここに記載)"""
        self.board = np.array(
            [
                [0, 0, 0, 0, 0, 0],
                [1, 5, 0, 0, 11, 15],
                [2, 6, 0, 0, 12, 16],
                [3, 7, 0, 0, 13, 17],
                [4, 8, 0, 0, 14, 18],
                [0, 0, 0, 0, 0, 0],
            ]
        )

        # IDは以下の通りに並べる(P1の駒が1~8、P2の駒が11~18)

        # [0, 0, 0, 0, 0,  0 ],
        # [1, 5, 0, 0, 11, 15],
        # [2, 6, 0, 0, 12, 16],
        # [3, 7, 0, 0, 13, 17],
        # [4, 8, 0, 0, 14, 18],
        # [0, 0, 0, 0, 0,  0 ],

    def move_pieces(self, move: str):
        """文字列(11rみたいなやつ)を受けて駒を実際に動かす"""
        if len(move) != 3:
            print("move_pieces:与えられた動作命令が不正です")
        else:
            char_list_move = list(move)
            # if 不正な手ではない
            # 移動先に駒があればデリートリストに追加しなくてはならない

            """駒の移動(移動対象,移動先 = 空, 移動対象)"""
            if char_list_move[2] == "u":
                (
                    self.board[int(char_list_move[0])][int(char_list_move[1])],
                    self.board[int(char_list_move[0]) - 1][int(char_list_move[1])],
                ) = (0, self.board[int(char_list_move[0])][int(char_list_move[1])])
            elif char_list_move[2] == "d":
                (
                    self.board[int(char_list_move[0])][int(char_list_move[1])],
                    self.board[int(char_list_move[0]) + 1][int(char_list_move[1])],
                ) = (0, self.board[int(char_list_move[0])][int(char_list_move[1])])
            elif char_list_move[2] == "r":
                (
                    self.board[int(char_list_move[0])][int(char_list_move[1])],
                    self.board[int(char_list_move[0])][int(char_list_move[1]) + 1],
                ) = (0, self.board[int(char_list_move[0])][int(char_list_move[1])])
            elif char_list_move[2] == "l":
                (
                    self.board[int(char_list_move[0])][int(char_list_move[1])],
                    self.board[int(char_list_move[0])][int(char_list_move[1]) - 1],
                ) = (0, self.board[int(char_list_move[0])][int(char_list_move[1])])
            else:
                print("与えられた動作命令の3文字目が不正です")

    def return_objective_board(self):
        """ボードをそのまま返す"""
        for row in self.board:
            for element in row:
                if element == 0:
                    print(element, end=" ")
                elif self.pieceArr[element] == -1:
                    print("r", end=" ")
                elif self.pieceArr[element] == 1:
                    print("b", end=" ")
            print()

    def return_player1_board(self):
        """プレイヤー1から見たボードを返す"""
        # 未実装
        for row in self.board:
            for element in row:
                if element == 0:
                    print(element, end=" ")
                elif self.pieceArr[element] == -1:
                    print("r", end=" ")
                elif self.pieceArr[element] == 1:
                    print("b", end=" ")
            print()

    def return_player2_board(self):
        """プレイヤー2から見たボードを返す"""
        # 未実装
        print(self.board)


# 駒にIDくっつけてボードではIDで管理が現実的かなぁ
class Piece:
    """駒の情報を保管"""

    def __init__(self, color: int):
        self.color = color  # 駒の色
        self.estimated_color = EstimatedColorUncertain  # 駒の色に対する推定値(駒推定の時に使うはず)


class Move:
    """プレイヤのとり得る手を管理するクラス"""

    def __init__(self, player_id: int, pieces: List[Piece]):
        if (player_id != 1) and (player_id != 2):
            print("プレイヤーが明示的に与えられていません")
        else:
            self.player_id = player_id
            self.pieces = pieces

    def check_regular_move(move: str) -> bool:
        """妥当な手かどうかチェック"""
        # そこに自分の駒が存在している
        # 移動先がボード内に収まっている(脱出は例外)
        # 移動先に自分の駒が存在しない

    def return_regular_move_list() -> List[str]:
        """妥当な手(不正でない手)を11nみたいな文字列のリストで返す(全探索で将来的に使うはず)"""
        for piece in self.pieces:
            print(piece.x)


class Game:
    """ゲーム全体を管理"""

    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]  # プレイに参加する2人のプレイヤを保存
        self.turn_player = NobodyPlayer  # 現在のターンプレイヤを保存
        self.first_turn_player = NobodyPlayer  # 先手のプレイヤを保存
        self.board = Board(player1, player2)  # 盤面(ボードの状態)を保存
        self.move_num = 0  # 何手目かを保存


class GameState:
    def __init__(self):
        super().__init__()

    def game_is_over() -> bool:
        """ゲームの終了を判定"""


def main():

    P1 = Player(1)
    P2 = Player(2)
    b = Board(P1, P2)
    b.reset_board()
    b.return_objective_board()

    print("u")
    b.move_pieces("11u")
    b.return_objective_board()

    print("d")
    b.reset_board()
    b.move_pieces("11d")
    b.return_objective_board()

    print("r")
    b.reset_board()
    b.move_pieces("11r")
    b.return_objective_board()

    print("l")
    b.reset_board()
    b.move_pieces("11l")
    b.return_objective_board()


if __name__ == "__main__":
    main()
