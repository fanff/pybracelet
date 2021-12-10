from PIL  import Image,ImageDraw2,ImageDraw

import numpy as np
from scipy.cluster.vq import kmeans,vq
import pandas as pd
import operator
import functools
import itertools

from collections import Counter

def minimalDistribution(nodes,colorCount):
    # calculate color distribution by column
    dists = nodes.groupby("colidx").apply(lambda x:Counter(x["cidx"]))

    # calculate minimal distribution
    minimalDist = {k:0 for k in range(colorCount)}

    for adist in dists.values:
        for k,v in adist.items():
            if v > minimalDist[k]:
                minimalDist[k]=v
    minimumWireCount = sum([v for cidx,v in minimalDist.items() ])

    return minimumWireCount,minimalDist



def colorIndexor_inapply(acol):
    """
    make a color indexor


    colorIndex = nodes.groupby("colidx").apply(colorIndexor).reset_index(drop=True)

    nodesUindexed = nodes.join(colorIndex.set_index(["colidx","cidx"]),on=["colidx","cidx"],rsuffix="lol")

    # back to original colors
    # nodesUindexed.join(colorIndex.set_index(["colidx","ucidx"]),on=["colidx","ucidx"],rsuffix="_back")
    """
    colindexor = acol.sort_values("rowidx").drop_duplicates("cidx",keep="first").reset_index(drop=True).reset_index()
    colindexor = colindexor.rename(columns={"index":"ucidx"})[["ucidx","colidx","cidx"]]
    return colindexor

def colorUIndex(nodes):
    colorIndex= nodes.groupby("colidx").apply(colorIndexor_inapply).reset_index(drop=True)
    return colorIndex

def re_index(nodes,colorIndex):
    """
    add new column with universal color index of each color
    :param nodes:
    :param colorIndex:
    :return:
    """
    return nodes.join(colorIndex.set_index(["colidx", "cidx"]), on=["colidx", "cidx"], rsuffix="lol")


def getColorConstraints(nodesUindexed):
    colorConstraints = nodesUindexed.groupby(["colidx"]).apply(lambda x: pd.DataFrame([ [tuple(x.sort_values("rowidx")["ucidx"].values),
    return colorConstraints                                                                              Counter(x["cidx"]),
                                                                                         Counter(x["ucidx"])]],
                                                                                      index = [x["colidx"].values[0]],


                                                                                      columns=["ucc","dc","ucidx"]))

    colorConstraints = colorConstraints.reset_index()#[["colidx","ucc"]]
    colorConstraints =colorConstraints.drop(columns=["level_1"])
    return colorConstraints


def bimage(nodes,wireCount,colormap):
    """
    image of bracelet
    """
    xscale = 40
    yscale = 60

    img = Image.new("RGB",((nodes["colidx"].max()+3)*xscale,int((wireCount//2+3)*yscale)),color="white")
    imgd = ImageDraw.Draw(img)


    for nidx,node in nodes.iterrows():
        c = (colormap[int(node.cidx)]*255).astype(np.uint8)

        x = (node.x+2) * xscale
        y = (node.y+1.5) * yscale

        xrad = xscale/1.1
        yrad = yscale/3
        imgd.ellipse((x-xrad,y-yrad,x+xrad,y+yrad), fill=tuple(c))
    return  img