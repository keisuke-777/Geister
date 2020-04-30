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

        # プレイヤーと駒が持つIDを紐づける
        self.player1_pieces_id_list = [1, 2, 3, 4, 5, 6, 7, 8]
        self.player2_pieces_id_list = [11, 12, 13, 14, 15, 16, 17, 18]

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
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ]
        )
        self.board[1][0] = self.player1_pieces_id_list[0]
        self.board[2][0] = self.player1_pieces_id_list[1]
        self.board[3][0] = self.player1_pieces_id_list[2]
        self.board[4][0] = self.player1_pieces_id_list[3]
        self.board[1][1] = self.player1_pieces_id_list[4]
        self.board[2][1] = self.player1_pieces_id_list[5]
        self.board[3][1] = self.player1_pieces_id_list[6]
        self.board[4][1] = self.player1_pieces_id_list[7]

        self.board[1][4] = self.player2_pieces_id_list[0]
        self.board[2][4] = self.player2_pieces_id_list[1]
        self.board[3][4] = self.player2_pieces_id_list[2]
        self.board[4][4] = self.player2_pieces_id_list[3]
        self.board[1][5] = self.player2_pieces_id_list[4]
        self.board[2][5] = self.player2_pieces_id_list[5]
        self.board[3][5] = self.player2_pieces_id_list[6]
        self.board[4][5] = self.player2_pieces_id_list[7]

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

    def check_regular_move(self, move: str, player_pieces_id_list: List[int]) -> bool:
        """妥当な手かどうかをチェック→妥当なら:trueを返す"""

        if len(move) != 3:
            print("与えられた動作命令の長さが不正です")
            return False
        else:
            char_list_move = list(move)

            # 0文字目と1文字目は数字じゃないと不正
            if not (char_list_move[0].isdecimal() and char_list_move[1].isdecimal()):
                print("0文字目と1文字目は数字(10進数)で与える必要があります。")
                return False

            # 移動前のマスがボードに収まっているか確認
            if (
                int(char_list_move[0]) <= -1
                or HeightOfBoard <= int(char_list_move[0])
                or int(char_list_move[1]) <= -1
                or WidthOfBoard <= int(char_list_move[1])
            ):
                print("与えられた動作命令の対象駒がボードからはみ出ています")
                return False

            # 移動前のマスに本当に自分の駒が存在するのかを確認する
            if not (
                self.board[int(char_list_move[0])][int(char_list_move[1])]
                in player_pieces_id_list
            ):
                print("与えられた座標には自身の駒が存在しません")
                return False

            # 移動先を計算
            if char_list_move[2] == "u":
                destination = [int(char_list_move[0]) - 1, int(char_list_move[1])]
            elif char_list_move[2] == "d":
                destination = [int(char_list_move[0]) + 1, int(char_list_move[1])]
            elif char_list_move[2] == "r":
                destination = [int(char_list_move[0]), int(char_list_move[1]) + 1]
            elif char_list_move[2] == "l":
                destination = [int(char_list_move[0]), int(char_list_move[1]) - 1]
            else:
                print("与えられた動作命令の3文字目が不正です(udrlしか受け付けません)")
                return False

            # 移動先に自分の駒が存在しているとアウト(自分の駒は殺せない)
            if self.board[destination[0]][destination[1]] in player_pieces_id_list:
                return False

            # 移動先がボード内に収まっていないならアウト(脱出は例外だけど処理は実装しないでいいかな(青駒が敵陣に潜り込んで殺されずにターン帰ってきたら勝利にするとか))
            if (
                destination[0] <= -1
                or HeightOfBoard <= destination[0]
                or destination[1] <= -1
                or WidthOfBoard <= destination[1]
            ):
                return False

            return True

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

    b.reset_board()
    print(b.check_regular_move("11l", b.player1_pieces_id_list))
    print(b.check_regular_move("11r", b.player1_pieces_id_list))
    print(b.check_regular_move("11u", b.player1_pieces_id_list))
    print(b.check_regular_move("11d", b.player1_pieces_id_list))
    print()
    print(b.check_regular_move("14l", b.player2_pieces_id_list))
    print(b.check_regular_move("14r", b.player2_pieces_id_list))
    print(b.check_regular_move("14u", b.player2_pieces_id_list))
    print(b.check_regular_move("14d", b.player2_pieces_id_list))
    print()
    print(b.check_regular_move("12d", b.player1_pieces_id_list))

    b.move_pieces("10u")
    print(b.check_regular_move("00u", b.player1_pieces_id_list))

    print(b.check_regular_move("00ぷ", b.player1_pieces_id_list))

    print(b.check_regular_move("いいね", b.player1_pieces_id_list))


if __name__ == "__main__":
    main()
