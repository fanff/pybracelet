import os
import FreeSimpleGUI as sg
from PIL import  Image
import io
import pandas as pd
from BData import BData, rowColToPixRect
from color_map import COLOR_MAP
import json

def popup_color_chooser(look_and_feel=None):
    """

    :return: Any(str, None) Returns hex string of color chosen or None if nothing was chosen
    """
    color_map = COLOR_MAP

    old_look_and_feel = None
    if look_and_feel is not None:
        old_look_and_feel = sg.CURRENT_LOOK_AND_FEEL
        sg.theme(look_and_feel)

    button_size = (1, 1)

    # button_size = (None,None)         # for very compact buttons

    def ColorButton(color):
        """
        A User Defined Element - returns a Button that configured in a certain way.
        :param color: Tuple[str, str] ( color name, hex string)
        :return: sg.Button object
        """
        return sg.B(button_color=('white', color[1]), pad=(0, 0), size=button_size, key=color, tooltip=f'{color[0]}:{color[1]}', border_width=0)

    num_colors = len(list(color_map.keys()))
    row_len = 40

    grid = [[ColorButton(list(color_map.items())[c + j * row_len]) for c in range(0, row_len)] for j in range(0, num_colors // row_len)]
    grid += [[ColorButton(list(color_map.items())[c + num_colors - num_colors % row_len]) for c in range(0, num_colors % row_len)]]

    layout = [[sg.Text('Pick a color', font='Def 18')]] + grid + \
             [[sg.Button('OK'), sg.T(size=(30, 1), key='-OUT-')]]

    window = sg.Window('Window Title', layout, no_titlebar=True, grab_anywhere=True, keep_on_top=True, use_ttk_buttons=True)
    color_chosen = None
    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'OK'):
            if event == sg.WIN_CLOSED:
                color_chosen = None
            break
        window['-OUT-'](f'You chose {event[0]} : {event[1]}')
        color_chosen = event[1]
    window.close()
    if old_look_and_feel is not None:
        sg.theme(old_look_and_feel)
    return color_chosen


def simpleSquare(color,pix=10):
    i = Image.new("RGB", size=(pix, pix),color=color)
    b = io.BytesIO()
    i.save(b, format="png")
    return b.getvalue()


def findNode(bdata,xclic,yclic):
    df = bdata.centers

    a:pd.Series = (df["xcenter"]-xclic)**2+(df["ycenter"]-yclic)**2

    node = df.loc[a.argmin()]

    colidx,rowidx = node.colidx, node.rowidx
    return colidx,rowidx




def redrawGraph(bdata,window,deep=True):
    gelem = window["-GRAPH-"]
    if deep:
        canvas_size = bdata.canvas_size()
        gelem.set_size(canvas_size)
        gelem.change_coordinates((0, 0), canvas_size)
        gelem.draw_rectangle((0, 0), canvas_size, fill_color=bdata.backGroundColor)

    for (colidx,rowidx),coloridx in bdata.nodes.items():
        if coloridx in bdata.colorRegistry:
            color = bdata.colorRegistry[coloridx]
            redrawNodeAt(gelem,colidx,rowidx,color,bdata.masterScale)
        else:
            raise ValueError(f"Color index {coloridx} not found in color registry.")
def redrawNodeAt(gelem,colidx,rowidx,color,masterScale):
    f, t = rowColToPixRect(colidx, rowidx,masterScale=masterScale)
    gelem.draw_oval(f, t, fill_color=color)



def main(args):
    if args.bracelet:
        with open(args.bracelet, "r") as fin:
            bdata = BData.fromJsonstr(fin.read())
    else:
        # Default bracelet data
        bdata = BData(wireCount=8,masterScale = 64)


    currentColorIdx = 1
    colorPickers = []
    for i,color in bdata.colorRegistry.items():
        l = [sg.Image(key=f"-CCHOICE{i}-",enable_events=True,
                    data=simpleSquare(color,pix=20)),
            sg.Button(f"{i}",
                key=f'Color Picker{i}',button_color=color)]
        colorPickers+= l


    layout = [  [sg.Input(key="-LOADNAME-"), sg.FileBrowse(),sg.B("load",key="-LOADFILE-")],
            
            [sg.Text("wire Count"),
                sg.Spin([6,8,10,12,14,16,18,20,22,24,26,28],
                                            initial_value = bdata.wireCount,
                                            key="-WCOUNT-",
                                            enable_events=True), sg.B(f'Background Color')],
                [colorPickers],

                [sg.Column([[sg.Graph(bdata.canvas_size(), (0, 0), bdata.canvas_size(), key='-GRAPH-',
                        change_submits=True, drag_submits=False,enable_events=True)]],scrollable=True,expand_y=True)],
            [sg.B("Save",key="-SAVEBUTTON-"), sg.In("current.json",key="-SAVENAME-")]]
    
    window = sg.Window('Bracelet Editor', layout,resizable=True)
    window.finalize()
    redrawGraph(bdata, window)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event.startswith('Color Picker'):
            window.hide()
            color_chosen = popup_color_chooser('Dark Blue 3')

            i = event.replace("Color Picker","")
            window[f'-CCHOICE{i}-'].update(data=simpleSquare(color_chosen,pix=20))
            window[event].update(button_color=color_chosen)

            bdata.colorRegistry[int(i)] = color_chosen
            redrawGraph(bdata, window)
            window.un_hide()
        elif event.startswith('-CCHOICE'):
            pass
            i = int(event.replace("-CCHOICE", "").replace("-",""))
            currentColorIdx = i

        elif event == "-WCOUNT-":

            newValue = values[event]
            bdata.newWireCount(newValue)
            redrawGraph(bdata,window)


        elif event == "-GRAPH-":
            clickCoord = values[event]

            x, y = clickCoord

            colidx,rowidx = findNode(bdata, x, y)

            bdata.setNodeColor(colidx,rowidx,currentColorIdx)
            color = bdata.colorRegistry[currentColorIdx]
            print(f'click {colidx, rowidx} ')

            redrawNodeAt(window["-GRAPH-"], colidx, rowidx, color,bdata.masterScale)
            #redrawGraph(bdata,window)
        elif event == 'Background Color':
            gelem = window[event]
            window.hide()
            color_chosen = popup_color_chooser('Dark Blue 3')
            gelem.update(button_color=color_chosen)
            window.un_hide()
            bdata.backGroundColor = color_chosen
            # redraw Canvas
            redrawGraph(bdata,window)

        elif event == "-SAVEBUTTON-":
            bname = values["-SAVENAME-"]
            bnamesan = bname.replace(" ","")

            if len(bnamesan)>0:
                s = bdata.toJson(indent=4)
                with open(bnamesan,"w") as fou:
                    fou.write(s)
        elif event == "-LOADFILE-":
            filename = values['-LOADNAME-']
            if filename.endswith(".json"):
                # if file exists, load it
                if os.path.exists(filename):
                    with open(filename, "r") as fin:
                        bdata = BData.fromJsonstr(fin.read())

                        redrawGraph(bdata, window, deep=False)
           

        else:
            print(f'The current look and feel = {sg.CURRENT_LOOK_AND_FEEL}')



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Bracelet Editor')
    parser.add_argument('bracelet', type=str, nargs='?', default=None,
                        help='Bracelet JSON file to load')
    
    args = parser.parse_args()
    main(args)