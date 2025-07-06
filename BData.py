from typing import Dict
import pandas as pd
import json

import collections


def rowColToPixRect(colidx, rowidx,masterScale):
    xpad = int(0.95*masterScale)
    ypad = int(0.9*masterScale)


    if colidx % 2 == 0:
        sx, sy = ((colidx//2)*masterScale,rowidx*masterScale)
        return (sx+xpad,sy+ypad) , (sx+masterScale-xpad,sy+masterScale-ypad)
    else:

        sx, sy = (((colidx // 2) * masterScale)+masterScale//2, rowidx * masterScale +masterScale//2)
        return (sx+xpad,sy+ypad) , (sx+masterScale-xpad,sy+masterScale-ypad)


class BData():

    def __init__(self,wireCount,colCount=50,masterScale=64):

        self.masterScale = masterScale
        
        self.wireCount = wireCount
        self.colCount = colCount 
        self.backGroundColor = '#000000'
        self.nodes=dict()
        self.maxColorCount = 12

        self.colorRegistry = {i:"#FFFFFF" for i in range(self.maxColorCount)}
        self.colorRegistry[1] = "#FF0000"
        self.colorRegistry[2] = "#00FF00"
        self.colorRegistry[3] = "#0000FF"
        self._initNodes()


    def newWireCount(self,wireCount):
        self.wireCount = wireCount
        self._initNodes()


    def canvas_size(self):
        return ((self.colCount//2+2)*self.masterScale,self.masterScale*self.wireCount//2)

    def setNodeColor(self,colidx, rowidx, currentColorIdx):
        self.nodes[(colidx, rowidx)] = currentColorIdx

    def _initNodes(self):

        knownnodes = self.nodes
        self.nodes = dict()
        centers = []
        for colidx in range(self.colCount):
            maxrowShit = 0 if colidx%2 == 0 else -1 # odd columns are shifted down by one row
            for rowidx in range(self.wireCount//2 + maxrowShit):

                idx = (colidx,rowidx)
                if idx in knownnodes:
                    self.nodes[idx] = knownnodes[idx]
                else:
                    self.nodes[idx] = 0

                f, t = rowColToPixRect(colidx, rowidx,self.masterScale)
                xcenter = (f[0] + t[0])//2
                ycenter = (f[1] + t[1])//2

                centers.append([colidx, rowidx,xcenter,ycenter])

        self.centers = pd.DataFrame(centers,columns=["colidx", "rowidx","xcenter","ycenter"])
    def toJson(self,indent=4) -> str:
        nodes = [[k1,k2,v] for (k1,k2),v in self.nodes.items()]
        return json.dumps((self.colorRegistry,nodes),indent=indent)
    
    @classmethod
    def fromJsonstr(cls,jsonstr) -> 'BData':
        """
        :param jsonstr: JSON string containing color registry and nodes
        :return: BData instance
        """
        # Parse the JSON string
        colorRegistry, nodes = json.loads(jsonstr)
        
        df_nodes = pd.DataFrame(nodes, columns=["colidx", "rowidx", "coloridx"])
        wireCount = (df_nodes["rowidx"].max()+1)*2

        # Create a new BData instance
        bdata = BData(wireCount=wireCount, masterScale=64)  # Assuming a default masterScale
        # Set the color registry    
        bdata.colorRegistry = {int(k):v for k,v in colorRegistry.items()}
        # Populate the nodes
        for colidx, rowidx, coloridx in nodes:
            bdata.nodes[(colidx, rowidx)] = coloridx    
        # Reinitialize centers based on the new nodes
        bdata._initNodes()
        return bdata


    def get_column(self,column_index):
        """
        Returns a list of color indices for the specified column.
        """
        column = []
        for (col_idx,row_idx),color_idx in self.nodes.items():
            if col_idx == column_index:
                column.append((col_idx,row_idx,color_idx))
        # sort column by row index
        column.sort(key=lambda x: x[1])
        return column
    
    
    def wire_assortment(self) -> Dict[int, int]:
        """
        Returns a dictionary with the count of each color used in the nodes.
        """

        assortment = {}
        # for every columns get the colors:
        for col_idx in range(self.colCount):
            column = self.get_column(col_idx)
            colors = [color_idx for _, _, color_idx in column]

            # Count occurrences of each color (group and count using python collections)
            color_count = collections.Counter(colors)

            # Add to the assortment dictionary if the color is not already present or if the count is higher then insert the new count
            for color_idx, count in color_count.items():
                if color_idx in assortment :
                    if assortment[color_idx] < count:
                        assortment[color_idx] = count
                else:
                    assortment[color_idx] = count

        return assortment


    def  validate_assortment(self,assortment: Dict[int,int]) -> bool:
        """
        Validates the assortment of colors against the maximum wire count.
        Returns True if valid, False otherwise.
        """
        # sum up all the counts in the assortment
        total_count = sum(assortment.values())
        # Check if the total count exceeds the maximum wire count
        return total_count <= self.wireCount

            
        