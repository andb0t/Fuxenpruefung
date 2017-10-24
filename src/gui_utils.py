import tkinter as tk

import i18n


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


def center_window(root, xdist=0, ydist=0):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # calculate position x and y coordinates
    x = (screen_width*xdist)
    y = (screen_height*ydist)
    root.geometry('+%d+%d' % (x, y))


class SimpleTable(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                relief = 'solid'
                if row > 0:
                    relief = 'groove'
                label = tk.Label(self, borderwidth=1, relief=relief)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value, **args):
        widget = self._widgets[row][column]
        widget.configure(text=value, **args)

    def headers(self, headers):
        for col, header in enumerate(headers):
            try:
                self.set(0, col, i18n.translate(header).capitalize(), font='bold')
            except AttributeError:
                self.set(0, col, header.capitalize(), font='bold')

    def data(self, scores, keys):
        for row, score in enumerate(scores):
            for col, val in enumerate(score.keys()):
                try:
                    self.set(row + 1, col, score[keys[col]])
                except IndexError:
                    break


def draw_table(master, canv, subBoxXMin, subBoxXMax, boxYMin, boxYMax, headers, values,
               title='table', tags='table', errText=None, nRows=None):
    distToSubBox = 1
    xCenter = (subBoxXMax + subBoxXMin) / 2
    vSpace = 15
    boxHeight = boxYMax - boxYMin

    canv.create_text(xCenter, boxYMin,
                     text=title, font='b', tags=(tags))
    canv.create_rectangle(subBoxXMin, boxYMin + vSpace, subBoxXMax, boxYMax + vSpace,
                          fill='black', tags=(tags + '_frame'))
    if not values:
        minY = boxYMin + vSpace + distToSubBox
        maxY = boxYMax + vSpace - distToSubBox
        bg = master.cget("background")
        canv.create_rectangle(subBoxXMin + distToSubBox, minY, subBoxXMax - distToSubBox, maxY,
                              fill=bg, tags=(tags + '_background'))
        if not errText:
            errText = 'Not available'
        canv.create_text(xCenter, (minY + maxY) / 2, text=errText, tags=(tags + '_empty'))
        return
    if nRows is None:
        nRows = len(values)
    t = SimpleTable(master, nRows, len(headers))
    t.headers(headers)
    t.data(values, headers)
    canv.create_window((subBoxXMin + distToSubBox, boxYMin + vSpace + distToSubBox),
                       window=t, anchor='nw',
                       width=subBoxXMax - subBoxXMin - distToSubBox,
                       height=boxHeight - distToSubBox,
                       tags=(tags + '_table'))


def main():
    print('Only plotting table and object!')
    root = tk.Tk()
    canv = tk.Canvas(root, highlightthickness=0)
    canv.pack(fill='both', expand=True)
    header = ['apple', 'orange', 'banana']
    data = [{'apple': [1, 2, 3], 'orange': [4, 5, 6], 'banana': [7, 8, 9]}]
    draw_table(root, canv, 0, 400, 0, 200, header, data)
    root.mainloop()
    root.destroy()


if __name__ == '__main__':
    main()
