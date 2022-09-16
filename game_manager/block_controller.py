#!/usr/bin/python3
# -*- coding: utf-8 -*-

from audioop import minmax
from datetime import datetime
import pprint
import copy
import math

class Block_Controller(object):

    # init parameter
    board_backboard = 0
    board_data_width = 0
    board_data_height = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    NextShape_class = 0
    BlockCount = 0
    GameLevel = 0
    BlockHigh = [0] * 10
    BlockDiff = [0] * 9
    BlockMax = 0
    DropMode = 10

    # GetNextMove is main function.
    # input
    #    GameStatus : this data include all field status, 
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : this data include next shape position and the other,
    #               if return None, do nothing to nextMove.
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()
        self.BlockCount += 1
        # print GameStatus
        print("=================================================>")
        #pprint.pprint(GameStatus, width = 61, compact = True)

        # current board info
        self.board_backboard = GameStatus["field_info"]["backboard"]
        # default board definition
        self.board_data_width = GameStatus["field_info"]["width"]
        self.board_data_height = GameStatus["field_info"]["height"]
        self.ShapeNone_index = GameStatus["debug_info"]["shape_info"]["shapeNone"]["index"]
        # nextShapeList
        E0ShapeDirectionRange = GameStatus["block_info"]["nextShapeList"]["element0"]["direction_range"]
        E1ShapeDirectionRange = GameStatus["block_info"]["nextShapeList"]["element1"]["direction_range"]
        E2ShapeDirectionRange = GameStatus["block_info"]["nextShapeList"]["element2"]["direction_range"]
        E0Shape_class = GameStatus["block_info"]["nextShapeList"]["element0"]["class"]
        E1Shape_class = GameStatus["block_info"]["nextShapeList"]["element1"]["class"]
        E2Shape_class = GameStatus["block_info"]["nextShapeList"]["element2"]["class"]
        E0Shape_index = GameStatus["block_info"]["nextShapeList"]["element0"]["index"]
        E1Shape_index = GameStatus["block_info"]["nextShapeList"]["element1"]["index"]
        E2Shape_index = GameStatus["block_info"]["nextShapeList"]["element2"]["index"]
        E0Shape_Count = 0   # roop count
        E1Shape_Count = 0   # roop count
        E2Shape_Count = 0   # roop count
        random_seed = GameStatus["debug_info"]["random_seed"]

        # print index & count
        print("index&count",E0Shape_index, self.BlockCount)
        # set BlockHigh
        self.SetBlockHigh(self.board_backboard)
        self.BlockMax = max(self.BlockHigh)
        print(self.BlockHigh)
        # Check Game Level
        if self.BlockCount == 1:
            if random_seed == 0:
                self.GameLevel = 1
            elif self.BlockMax == 0:
                self.GameLevel = 2
            else:
                self.GameLevel = 3
            #print("GameLevel",self.GameLevel)

        # select Drop Mode
        if self.GameLevel == 1:
            if self.BlockCount > 160:
                self.DropMode = 11
        elif self.GameLevel == 2:
            if self.BlockCount == 1:
                self.DropMode = 20
            elif self.DropMode == 20:
                if self.BlockMax > 15:
                    self.DropMode = 21
            elif self.DropMode == 21:
                if self.BlockMax < 12:
                    self.DropMode = 20
        elif self.GameLevel == 3:
            if self.BlockCount == 1:
                self.DropMode = 31
            elif self.DropMode == 30:
                if self.BlockMax > 15:
                    self.DropMode = 31
            elif self.DropMode == 31:
                if self.BlockMax < 12:
                    self.DropMode = 30
        print("DropMode",self.DropMode)        

        # search best nextMove -->
        strategy = None
        LatestEvalValue = -100000
        # serch preparation
        if E0Shape_index == 1:
            E0ShapeDirectionRange = (0,)
        else:
            E0Shape_Count = len(E0ShapeDirectionRange)
        if E1Shape_index == 1:
            E1ShapeDirectionRange = (0,)
        else:
            E1Shape_Count = len(E1ShapeDirectionRange)
        if E2Shape_index == 1:
            E2ShapeDirectionRange = (0,)
        else:
            E2Shape_Count = len(E2ShapeDirectionRange)
        

        # search with element0 block Shape
        for direction0 in E0ShapeDirectionRange:
            # search with x range
            if E0Shape_index == 1:
                x0Min = self.Isearch(self.board_backboard)
                x0MinMax = (x0Min,)
            else:
                x0Min, x0Max = self.getSearchXRange(E0Shape_class, direction0)
                x0MinMax = range(x0Min, x0Max)
            for x0 in x0MinMax:
                # get board data, as if dropdown block
                board0 = self.getBoard(self.board_backboard, E0Shape_class, direction0, x0)

                # search with element1 block Shape
                for direction1 in E1ShapeDirectionRange:
                    # search with x range
                    if E1Shape_index == 1:
                        x1Min = self.Isearch(board0)
                        x1MinMax = (x1Min,)
                    else:
                        x1Min, x1Max = self.getSearchXRange(E1Shape_class, direction1)
                        x1MinMax = range(x1Min, x1Max)
                    for x1 in x1MinMax:
                        # get board data, as if dropdown block
                        board1 = self.getBoard(board0, E1Shape_class, direction1, x1)

                        if (E0Shape_Count+E1Shape_Count+E2Shape_Count) > 8:
                            #print(direction0,x0,direction1,x1)
                            # evaluate board
                            EvalValue = self.calcEvaluationValueSample(board1)
                            # update best move
                            if EvalValue > LatestEvalValue:
                                strategy = (direction0, x0, 1, 1)
                                LatestEvalValue = EvalValue
                        else:
                            # search with element2 block Shape
                            for direction2 in E2ShapeDirectionRange:
                                # search with x range
                                if E2Shape_index == 1:
                                    x2Min = self.Isearch(board1)
                                    x2MinMax = (x2Min,)
                                else:
                                    x2Min, x2Max = self.getSearchXRange(E2Shape_class, direction2)
                                    x2MinMax = range(x2Min, x2Max)
                                for x2 in x2MinMax:
                                    # get board data, as if dropdown block
                                    board2 = self.getBoard(board1, E2Shape_class, direction2, x2)

                                    #print(direction0,x0,direction1,x1,direction2,x2)
                                    # evaluate board
                                    EvalValue = self.calcEvaluationValueSample(board2)
                                    # update best move
                                    if EvalValue > LatestEvalValue:
                                        strategy = (direction0, x0, 1, 1)
                                        LatestEvalValue = EvalValue

        #print(LatestEvalValue)
        #print(E0Shape_Count,E1Shape_Count,E2Shape_Count)
        print("===", datetime.now() - t1)
        nextMove["strategy"]["direction"] = strategy[0]
        nextMove["strategy"]["x"] = strategy[1]
        nextMove["strategy"]["y_operation"] = strategy[2]
        nextMove["strategy"]["y_moveblocknum"] = strategy[3]
        #print("nextMove",strategy[0],strategy[1])
        #print(nextMove)
        return nextMove

    def getSearchXRange(self, Shape_class, direction):
        #
        # get x range from shape direction.
        #
        minX, maxX, _, _ = Shape_class.getBoundingOffsets(direction) # get shape x offsets[minX,maxX] as relative value.
        xMin = -1 * minX
        if self.DropMode == 21 or self.DropMode == 31:
            xMax = self.board_data_width - maxX
        else:
            xMax = self.board_data_width - maxX-1                           # right side 9Line
        return xMin, xMax

    def getShapeCoordArray(self, Shape_class, direction, x, y):
        #
        # get coordinate array by given shape.
        #
        coordArray = Shape_class.getCoords(direction, x, y) # get array from shape direction, x, y.
        return coordArray

    def getBoard(self, board_backboard, Shape_class, direction, x):
        # 
        # get new board.
        #
        # copy backboard data to make new board.
        # if not, original backboard data will be updated later.
        board = copy.deepcopy(board_backboard)
        _board = self.dropDown(board, Shape_class, direction, x)
        return _board

    def dropDown(self, board, Shape_class, direction, x):
        # 
        # internal function of getBoard.
        # -- drop down the shape on the board.
        # 
        dy = self.board_data_height - 1
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        # update dy
        for _x, _y in coordArray:
            _yy = 0
            while _yy + _y < self.board_data_height and (_yy + _y < 0 or board[(_y + _yy) * self.board_data_width + _x] == self.ShapeNone_index):
                _yy += 1
            _yy -= 1
            if _yy < dy:
                dy = _yy
        # get new board
        _board = self.dropDownWithDy(board, Shape_class, direction, x, dy)
        return _board

    def dropDownWithDy(self, board, Shape_class, direction, x, dy):
        #
        # internal function of dropDown.
        #
        _board = board
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        for _x, _y in coordArray:
            _board[(_y + dy) * self.board_data_width + _x] = Shape_class.shape
        return _board

    def calcEvaluationValueSample(self, board):
        #
        # sample function of evaluate board.
        #
        width = self.board_data_width
        height = self.board_data_height

        # evaluation paramters
        ## lines to be removed
        fullLines = 0
        ## number of holes or blocks in the line.
        nHoles = 0
        #nIsolatedBlocks = 0
        ## absolute differencial value of MaxY
        #absDy = 0
        diff4count = 0
        ##  block difference edges
        DiffEdgeCount = 0
        ## how blocks are accumlated
        BlockMaxY = [0] * width
        holeCandidates = [0] * width
        holeConfirm = [0] * width

        ### check board
        # each y line
        for y in range(height - 1, 0, -1):
            hasHole = False
            hasBlock = False
            # each x line
            for x in range(width):
                ## check if hole or block..
                if board[y * self.board_data_width + x] == self.ShapeNone_index:
                    # hole
                    hasHole = True
                    holeCandidates[x] += 1  # just candidates in each column..
                else:
                    # block
                    hasBlock = True
                    BlockMaxY[x] = height - y                # update blockMaxY
                    if holeCandidates[x] > 0:
                        holeConfirm[x] += holeCandidates[x]  # update number of holes in target column..
                        holeCandidates[x] = 0                # reset
                    #if holeConfirm[x] > 0:
                    #    nIsolatedBlocks += 1                 # update number of isolated blocks

            if hasBlock == True and hasHole == False:
                # filled with block
                fullLines += 1
            elif hasBlock == True and hasHole == True:
                # do nothing
                pass
            elif hasBlock == False:
                # no block line (and ofcourse no hole)
                pass

        # nHoles
        for x in holeConfirm:
            nHoles += abs(x)

        ### absolute differencial value of MaxY
        BlockMaxDy = []
        for i in range(len(BlockMaxY) - 1):
            val = BlockMaxY[i] - BlockMaxY[i+1]
            BlockMaxDy += [val]
        for x in BlockMaxDy:
            #absDy += abs(x)
            if abs(x) >= 4:
                diff4count += 1

        # standard deviation
        average = sum(BlockMaxY)/len(BlockMaxY)
        num = 1
        zure_sum = 0.0
        for MaxY in BlockMaxY:
            zure = round((MaxY - average)**2,1)
            # zure = (score - average)**2
            num = num + 1
            zure_sum = zure_sum + zure
        variance = zure_sum/len(BlockMaxY)
        standard_deviation = math.sqrt(variance)

        # Check the difference edges
        if (BlockMaxY[0] + 3) <= BlockMaxY[1]:
            DiffEdgeCount = +(BlockMaxY[1]-BlockMaxY[0])/4
        if (BlockMaxY[self.board_data_width-2] + 3) <= BlockMaxY[self.board_data_width-3]:
            DiffEdgeCount = +(BlockMaxY[self.board_data_width-3] - BlockMaxY[self.board_data_width-2])/4

        # calc Evaluation Value
        score = 0
        if self.DropMode == 10:
            #score = score + fullLines * 10.0           # try to delete line 
            score = score - nHoles * 100.0              # try not to make hole
            #score = score - nIsolatedBlocks * 5.0      # try not to make isolated block
            score = score - standard_deviation * 1.0    # standard deviation
            #score = score - absDy * 0.000000001        # try to put block smoothly
            score = score - diff4count * 0.00001        # difference 4block count
            score = score - DiffEdgeCount * 0.0001
        elif self.DropMode == 11:
            #score = score + fullLines * 10.0           # try to delete line 
            score = score - nHoles * 100.0              # try not to make hole
            #score = score - nIsolatedBlocks * 5.0      # try not to make isolated block
            score = score - standard_deviation * 1.0    # standard deviation
            #score = score - absDy * 0.000000001        # try to put block smoothly
            score = score - diff4count * 0.00001        # difference 4block count
            score = score - DiffEdgeCount * 0.2
        elif self.DropMode == 20:
            #score = score + fullLines * 10.0           # try to delete line 
            score = score - nHoles * 100.0              # try not to make hole
            #score = score - nIsolatedBlocks * 5.0      # try not to make isolated block
            score = score - standard_deviation * 1.0    # standard deviation
            #score = score - absDy * 0.000000001        # try to put block smoothly
            score = score - diff4count * 0.00001        # difference 4block count
            score = score - DiffEdgeCount * 0.01
        elif self.DropMode == 21:
            score = score + fullLines * 10.0           # try to delete line 
            score = score - nHoles * 0.5              # try not to make hole
            #score = score - nIsolatedBlocks * 5.0      # try not to make isolated block
            score = score - standard_deviation * 1.0    # standard deviation
            #score = score - absDy * 0.000000001        # try to put block smoothly
            score = score - diff4count * 1.0        # difference 4block count
            score = score - DiffEdgeCount * 1.0
        elif self.DropMode == 30:
            #score = score + fullLines * 10.0           # try to delete line 
            score = score - nHoles * 100.0              # try not to make hole
            #score = score - nIsolatedBlocks * 5.0      # try not to make isolated block
            score = score - standard_deviation * 1.0    # standard deviation
            #score = score - absDy * 0.000000001        # try to put block smoothly
            score = score - diff4count * 0.00001        # difference 4block count
            score = score - DiffEdgeCount * 0.2
        else:                                           #         self.DropMode == 31:
            score = score + fullLines * 10.0           # try to delete line 
            score = score - nHoles * 0.5              # try not to make hole
            #score = score - nIsolatedBlocks * 5.0      # try not to make isolated block
            score = score - standard_deviation * 1.0    # standard deviation
            #score = score - absDy * 0.000000001        # try to put block smoothly
            score = score - diff4count * 1.0        # difference 4block count
            score = score - DiffEdgeCount * 1.0

        #print(score, nHoles, standard_deviation, DiffEdgeCount)
        return score

    def Isearch(self, board):
        #
        # sample function of evaluate board.
        #
        width = self.board_data_width
        height = self.board_data_height

        # evaluation paramters
        BlockMaxY = [0] * width
        MinX = 0
        DiffX= width
        MinMax4Count = 0
        MinValue = height

        ### check board
        # each y line
        for y in range(height - 1, 0, -1):
            # each x line
            for x in range(width):
                ## check if hole or block..
                if board[y * self.board_data_width + x] == self.ShapeNone_index:
                    # hole
                    pass
                else:
                    # block
                    BlockMaxY[x] = height - y                # update blockMaxY

        # MinMaxCheck
        for x in range(width):
            sub = BlockMaxY[x] - min(BlockMaxY)
            if self.DropMode == 21 or self.DropMode == 31:
                if sub >= 2:
                    MinMax4Count +=1
            else:
                if sub >= 4:
                    MinMax4Count +=1
            # Last X
            if x == width-1:
                if MinMax4Count >= width-1:                     # 4line 
                    if sub == 0:
                        MinX = width-1
            else:
                if MinValue > BlockMaxY[x]:                     # >:left side >=:right side
                    MinValue = BlockMaxY[x]
                    MinX = x
                #if(BlockMaxY[x] - BlockMaxY[x+1]) > 4:         # difference 4 Block Over
                #    DiffX = x+1
        if MinX != width-1:
            if DiffX < width-1:
                MinX = DiffX

        #print("I",MinMax4Count,MinX)
        return MinX

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

        # Diff check
        for x in range(width-1):
            self.BlockDiff[x] = self.BlockHigh[x+1] - self.BlockHigh[x]
        #print("diff=",self.BlockDiff)

        return

BLOCK_CONTROLLER = Block_Controller()
