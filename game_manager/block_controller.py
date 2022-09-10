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
    GameLevel = 0
    BlockHigh = [0] * 10
    BlockDiff = [0] * 9
    BlockMax = 0
    BlockMin = 0

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
        #pprint.pprint(GameStatus, width = 61, compact = True)

        # current board info
        self.board_backboard = GameStatus["field_info"]["backboard"]
        # default board definition
        self.board_data_width = GameStatus["field_info"]["width"]
        self.board_data_height = GameStatus["field_info"]["height"]
        # nextShapeList
        E0Shape_index = GameStatus["block_info"]["nextShapeList"]["element0"]["index"]
        E1Shape_index = GameStatus["block_info"]["nextShapeList"]["element1"]["index"]
        E2Shape_index = GameStatus["block_info"]["nextShapeList"]["element2"]["index"]
        E3Shape_index = GameStatus["block_info"]["nextShapeList"]["element3"]["index"]
        E4Shape_index = GameStatus["block_info"]["nextShapeList"]["element4"]["index"]
        E5Shape_index = GameStatus["block_info"]["nextShapeList"]["element5"]["index"]

        # set BlockHigh
        self.SetBlockHigh(self.board_backboard)
        print(self.BlockHigh)
        self.BlockMax = max(self.BlockHigh)
        self.BlockMin = min(self.BlockHigh)

        # search best nextMove -->
        MinIndex = self.BlockHigh.index(self.BlockMin)
        MaxIndex = self.BlockHigh.index(self.BlockMax)

        if E0Shape_index == 1:      # I
            strategy = ( 0 , MinIndex , 1 , 1 )
        elif  E0Shape_index == 2:   # L
            if MinIndex == 0:
                if self.BlockHigh[0] == self.BlockHigh[1]:
                    if self.BlockHigh[0] == self.BlockHigh[2]:
                        strategy = ( 3 , MinIndex+1 , 1 , 1 )
                    else:
                        strategy = ( 0 , MinIndex , 1 , 1 )
                else:
                    strategy = ( 1 , MinIndex , 1 , 1 )
            elif MinIndex == 9:
                strategy = ( 2 , MinIndex , 1 , 1 )
            elif MinIndex == 8:
                if self.BlockHigh[8] == self.BlockHigh[9]:
                    strategy = ( 0 , MinIndex , 1 , 1 )
                else:
                    strategy = ( 2 , MinIndex , 1 , 1 )
            else:
                if self.BlockHigh[MinIndex] == self.BlockHigh[MinIndex+1]:
                    if self.BlockHigh[MinIndex] == self.BlockHigh[MinIndex+2]:
                        strategy = ( 3 , MinIndex+1 , 1 , 1 )
                    else:
                        strategy = ( 0 , MinIndex , 1 , 1 )
                else:
                    strategy = ( 2 , MinIndex , 1 , 1 )
        elif  E0Shape_index == 3:   # J
            if MinIndex == 0:
                if self.BlockHigh[0] == self.BlockHigh[1]:
                    if self.BlockHigh[0] == self.BlockHigh[2]:
                        strategy = ( 1 , MinIndex+1 , 1 , 1 )
                    else:
                        strategy = ( 0 , MinIndex+1 , 1 , 1 )
                else:
                    strategy = ( 2 , MinIndex , 1 , 1 )
            elif MinIndex == 9:
                strategy = ( 3 , MinIndex , 1 , 1 )
            elif MinIndex == 8:
                if self.BlockHigh[8] == self.BlockHigh[9]:
                    strategy = ( 0 , MinIndex+1 , 1 , 1 )
                else:
                    strategy = ( 2 , MinIndex , 1 , 1 )
            else:
                if self.BlockHigh[MinIndex] == self.BlockHigh[MinIndex+1]:
                    if self.BlockHigh[MinIndex] == self.BlockHigh[MinIndex+2]:
                        strategy = ( 1 , MinIndex+1 , 1 , 1 )
                    else:
                        strategy = ( 0 , MinIndex+1 , 1 , 1 )
                else:
                    strategy = ( 2 , MinIndex , 1 , 1 )
        elif  E0Shape_index == 4:   # T
            if MinIndex == 0:
                if self.BlockHigh[0] == self.BlockHigh[1]:
                    if self.BlockHigh[0] == self.BlockHigh[2]:
                        strategy = ( 3 , MinIndex+1 , 1 , 1 )
                    else:
                        strategy = ( 2 , MinIndex+1 , 1 , 1 )       # Hole
                else:
                    strategy = ( 0 , MinIndex , 1 , 1 )
            elif MinIndex == 9:
                strategy = ( 2 , MinIndex , 1 , 1 )
            elif MinIndex == 8:
                if (self.BlockHigh[9] - self.BlockHigh[8]) == 1:
                    strategy = ( 0 , MinIndex , 1 , 1 )
                elif self.BlockHigh[9] > self.BlockHigh[7]:
                    strategy = ( 2 , MinIndex , 1 , 1 )
                else: 
                    strategy = ( 0 , MinIndex , 1 , 1 )
            else:
                if self.BlockHigh[MinIndex] == self.BlockHigh[MinIndex+1]:
                    if self.BlockHigh[MinIndex] == self.BlockHigh[MinIndex+2]:
                        strategy = ( 3 , MinIndex+1 , 1 , 1 )
                    elif self.BlockHigh[MinIndex+2] > self.BlockHigh[MinIndex-1]:
                        strategy = ( 2 , MinIndex , 1 , 1 )
                    else:
                        strategy = ( 0 , MinIndex+1 , 1 , 1 )
                elif self.BlockHigh[MinIndex+1] > self.BlockHigh[MinIndex-1]:           
                    strategy = ( 2 , MinIndex , 1 , 1 )
                else:
                    strategy = ( 0 , MinIndex , 1 , 1 )                    
        elif  E0Shape_index == 5:   # O
            if (MinIndex != 9) and (self.BlockHigh[MinIndex] == self.BlockHigh[MinIndex+1]):
                strategy = ( 0 , MinIndex , 1 , 1 )
            else:
                BlockValue = []
                for x0 in range(8):
                    if self.BlockHigh[x0] == self.BlockHigh[x0+1]:
                        BlockValue.append(self.BlockHigh[x0]+2)
                    else:
                        BlockValue.append(self.BlockHigh[x0]+8)
                strategy = ( 0 , BlockValue.index(min(BlockValue)) , 1 , 1 )
        elif  E0Shape_index == 6:   # S
            if MinIndex == 0:
                if (self.BlockHigh[0] == self.BlockHigh[1]) and ((self.BlockHigh[2]-self.BlockHigh[1]) == 1 ):
                    strategy = ( 0 , 1 , 1 , 1 )
                else:
                    for x0 in range(8):
                        if self.BlockHigh[x0] > self.BlockHigh[x0+1]:
                            break
                    strategy = ( 1 , x0 , 1 , 1 )
            elif MaxIndex == 9:
                if (self.BlockDiff[8]) == -1:
                    strategy = ( 1 , 8 , 1 , 1 )
                else:
                    BlockValue = []
                    for x0 in range(8):
                        if self.BlockDiff[x0] < 0:
                            BlockValue.append(self.BlockHigh[x0]+(self.BlockDiff[x0]*-1-1)*4)
                        else:
                            BlockValue.append(self.BlockHigh[x0]+8)
                    strategy = ( 1 , BlockValue.index(min(BlockValue)) , 1 , 1 )
            else:
                if self.BlockDiff[MinIndex-1] == -1:
                    strategy = ( 1 , MinIndex-1 , 1 , 1 )
                else:
                    BlockValue = []
                    for x0 in range(8):
                        if self.BlockDiff[x0] < 0:
                            BlockValue.append(self.BlockHigh[x0]+(self.BlockDiff[x0]*-1-1)*4)
                        else:
                            BlockValue.append(self.BlockHigh[x0]+8)
                    strategy = ( 1 , BlockValue.index(min(BlockValue)) , 1 , 1 )
        elif  E0Shape_index == 7:   # Z
            if MinIndex == 9:
                BlockValue = []
                for x0 in range(8):
                    if self.BlockDiff[x0] > 0:
                        BlockValue.append(self.BlockHigh[x0]+(self.BlockDiff[x0]-1)*4)
                    else:
                        BlockValue.append(self.BlockHigh[x0]+8)
                strategy = ( 1 , BlockValue.index(min(BlockValue)) , 1 , 1 )
            else:
                if self.BlockDiff[MinIndex] == 1:
                    strategy = ( 1 , MinIndex , 1 , 1 )
                else:
                    BlockValue = []
                    for x0 in range(8):
                        if self.BlockDiff[x0] > 0:
                            BlockValue.append(self.BlockHigh[x0]+(self.BlockDiff[x0]-1)*4)
                        else:
                            BlockValue.append(self.BlockHigh[x0]+8)
                    strategy = ( 1 , BlockValue.index(min(BlockValue)) , 1 , 1 )
 
        print("Index=",E0Shape_index)
        print("d/x=",strategy[0],strategy[1])
        self.BlockCount += 1

        nextMove["strategy"]["direction"] = strategy[0]
        nextMove["strategy"]["x"] = strategy[1]
        nextMove["strategy"]["y_operation"] = strategy[2]
        nextMove["strategy"]["y_moveblocknum"] = strategy[3]
        # search best nextMove <--

        # return nextMove
        print("===", datetime.now() - t1)
        #print(nextMove)
        return nextMove

    def SetBlockHigh(self, board):
        #
        # Stores the height of the Block in BlockHigh[].
        #
        width = self.board_data_width
        height = self.board_data_height
        self.BlockHigh = [0] * width

        ### check board
        # each x line
        for x in range(width):
            # each y line
            for y in range(height):
                if board[y * self.board_data_width + x] == self.ShapeNone_index:
                    # hole
                    pass
                else:
                    # block
                    self.BlockHigh[x] = height - y                # update blockHigh
                    break
        for x in range(width-1):
            self.BlockDiff[x] = self.BlockHigh[x+1] - self.BlockHigh[x]
        return

BLOCK_CONTROLLER = Block_Controller()

