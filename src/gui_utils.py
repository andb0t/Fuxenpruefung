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
