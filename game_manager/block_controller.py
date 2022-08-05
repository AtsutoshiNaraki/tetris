#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import random

class Block_Controller(object):

    # init parameter
    board_backboard = 0
    board_data_width = 0
    board_data_height = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    NextShape_class = 0
    CurrentShape_index = 0
    BlockCount =0

    FixMove = (
        #D,X   D,X   D,X   D,X   D,X   D,X   D,X
        #1I    2L    3J    4T    5O    6S    7Z
        (0,0),(0,1),(0,4),(3,6),(0,2),(1,7),(1,5),      # 1Cycle
        (0,8),(0,4),(3,6),(2,1),(0,2),(0,3),(1,0),      # 2
        (0,9),(1,3),(1,6),(3,7),(0,5),(1,7),(1,0),      # 3
        (0,0),(1,5),(0,3),(2,2),(0,5),(1,7),(1,1),      # 4
        (0,9),(0,0),(3,7),(2,4),(0,1),(1,4),(0,6),      # 5
        (0,3),(3,1),(1,5),(0,3),(0,0),(1,7),(1,2),      # 6
        (0,9),(0,0),(3,7),(0,5),(0,1),(1,6),(1,4),      # 7
        (0,9),(2,8),(1,7),(0,4),(0,0),(1,2),(0,7),      # 8
        (0,9),(1,6),(3,2),(0,4),(0,6),(0,3),(1,0),      # 9
        (0,8),(1,6),(3,7),(0,2),(0,7),(0,5),(1,0),      # 10
        (0,9),(1,7),(2,5),(0,0),(0,3),(1,1),(0,3),      # 11
        (0,9),(1,0),(0,8),(3,6),(0,1),(1,3),(0,4),      # 12
        (0,9),(3,3),(2,0),(1,7),(0,0),(0,3),(1,5),      # 13
        (0,8),(2,7),(2,5),(2,2),(0,3),(1,6),(1,0),      # 14
        (0,9),(3,3),(2,5),(3,5),(0,2),(1,7),(1,0),      # 15
        (0,9),(1,0),(1,0),(2,8),(0,3),(0,7),(0,5),      # 16
        (0,9),(3,2),(1,0),(3,7),(0,4),(1,7),(0,1),      # 17
        (0,6),(1,4),(3,1),(0,5),(0,3),(1,7),(0,6),      # 18
        (0,9),(2,8),(0,2),(0,0),(0,3),(1,0),(0,2),      # 19
        (0,9),(3,7),(1,1),(0,7),(0,4),(1,5),(1,3),      # 20
        (0,9),(3,2),(3,5),(2,8),(0,0),(0,7),(1,2),      # 21
        (0,8),(0,4),(1,0),(3,2),(0,5),(1,6),(1,1),      # 22
        (0,9),(3,4),(2,0),(2,7),(0,3),(1,4),(1,6),      # 23
        (0,9),(0,0),(0,3),(0,5),(0,1),(1,3),(0,6),      # 24
        (0,8),(1,5),(1,1),(0,2),(0,7),(1,0),(0,3),      # 25
        (0,9),(2,9),(1,6),(2,1),(0,7)                   # 26
    )

    # GetNextMove is main function.
    # input
    #    GameStatus : this data include all field status, 
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : this data include next shape position and the other,
    #               if return None, do nothing to nextMove.
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()

        # print GameStatus
        print("=================================================>")
        pprint.pprint(GameStatus, width = 61, compact = True)

        # current shape info
        self.CurrentShape_index = GameStatus["block_info"]["currentShape"]["index"]

        # search best nextMove -->
        if self.BlockCount < len(self.FixMove):
            strategy = (self.FixMove[self.BlockCount][0],self.FixMove[self.BlockCount][1], 1, 1)
            print("Cycle=",int(self.BlockCount/7) +1)
            print("Index=",self.CurrentShape_index)
            print("Move=",self.FixMove[self.BlockCount])
        self.BlockCount += 1

        nextMove["strategy"]["direction"] = strategy[0]
        nextMove["strategy"]["x"] = strategy[1]
        nextMove["strategy"]["y_operation"] = strategy[2]
        nextMove["strategy"]["y_moveblocknum"] = strategy[3]
        # search best nextMove <--

        # return nextMove
        print("===", datetime.now() - t1)
        print(nextMove)
        return nextMove

BLOCK_CONTROLLER = Block_Controller()

