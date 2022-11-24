import sys
import gui
import interface

import chess, chess.engine

from PyQt5 import QtCore
def getArgs():
    """
        Returns a tuple with [0] as wslink and [1] as stockfish binary link
        from cli args
    """
    return (sys.argv[1], sys.argv[2])

isWhite = 0
def main():
    data = getArgs()
    ws_link = data[0]
    fish_loc = data[1]
    chengine = chess.engine.SimpleEngine.popen_uci(fish_loc)
    # engine.uci()
    window = gui.Gui()
    inter = interface.Interface(ws_link)
    turnStr = [" b", " w"]
    def update():
        global isWhite
        isWhite = not isWhite
        fen =  inter.get_data()
        board = chess.Board(fen + turnStr[isWhite] + " KQkq - 0 1")
        chengine.position(board)
        result = str(chengine.go()[0])
        window.updateBoard(board)
        window.suggestMove(result)
        timer.start(1000)
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.setSingleShot(True)
    timer.start(1000)
    window.start()

if __name__ == "__main__":
    main()
