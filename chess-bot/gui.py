import sys
import chess, chess.uci, chess.svg
from PyQt5 import QtSvg, QtWidgets, QtCore

class BoardWidget(QtSvg.QSvgWidget):
    """
        A widget to display and handle generated python-chess chessboard svgs
    """
    def __init__(self, svgString=None):
        """
            Returns a BoardWidget object with either a svg string or file loaded
        """
        super().__init__()
        if svgString :
            if ".svg" in svgString:
                super().load(svgString)
            else:
                super().load(bytes(svgString, 'utf8'))
    def load(self, svgString):
        """
            Loads a svg string or svg file into the widget
        """
        if ".svg" in svgString:
            super().load(svgString)
        else:
            super().load(bytes(svgString, 'utf8'))
    def adjustSize(self):
        """
            Adjusts the size and location of the widget
        """
        size = super().sizeHint()
        super().setGeometry(400,100,size.width()*1.5, size.height()*1.5)

class Gui(object):
    """
        A gui to display the next best move on a chessboard.
    """
    vals = {x:i for i,x in enumerate(chess.SQUARE_NAMES)}
    def __init__(self, board=chess.BaseBoard()):
        """
            Returns a Gui object ----
        """
        self.app = QtWidgets.QApplication(sys.argv)
        self.board = board
        self.svg = chess.svg.board(board=self.board)
        self.svgWidget = BoardWidget(self.svg)
        self.svgWidget.adjustSize()
        self.svgWidget.setWindowTitle("chess-bot")
    def updateBoard(self, board):
        """
            Update chessboard using chess.Board
        """
        self.board = board
        self.svg = chess.svg.board(board=self.board)
        self.svgWidget.load(self.svg)
    def suggestMove(self, move):
        """
            Draw an arrow according to the chess move string
        """
        arrows = [((Gui.vals[move[:2]]), (Gui.vals[move[2:]]))]
        self.svg = chess.svg.board(board=self.board,arrows=arrows)
        self.svgWidget.load(self.svg)
    def exec(self):
        """
            Starts QApplication main event loop, that's it
        """
        self.app.exec_()
