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

def main():
    data = getArgs()
    ws_link = data[0]
    fish_loc = data[1]
    chengine = chess.engine.SimpleEngine.popen_uci(fish_loc)
    window = gui.Gui()
    inter = interface.Interface(ws_link)
    turnStr = [" w", " b"]
    def update():
        try:
            fen, isWhite =  inter.get_data()
            board = chess.Board(fen + turnStr[isWhite] + " KQkq - 0 1")
            info = chengine.analyse(board, chess.engine.Limit(time=0.1))
            result = str(info["pv"][0].uci())
            window.updateBoard(board)
            window.suggestMove(result)
        except:
            pass
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(100)
    window.start()

if __name__ == "__main__":
    main()
