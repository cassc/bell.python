from bell.consts import SCREEN_HEIGHT, SCREEN_WIDTH

def make_text(content, x, y, clear=False, max_width=SCREEN_WIDTH, color='black', font_size=12):
    return {'type': 'text-msg',
            'clear': clear,
            'data': {'content': content,
                     'x': x,
                     'y': y,
                     'max-width': max_width,
                     'color': color,
                     'font-size': font_size,
            },}

def make_rect(x, y, w, h, clear=False, fill=False, color='black'):
    return {'type': 'rect',
            'clear': clear,
            'data': {'x': x,
                     'y': y,
                     'w': w,
                     'h': h,
                     'fill': fill,
                     'color': color,
            },}


def make_circle(x, y, r, clear=False, fill=False, color='black'):
    return {'type': 'circle',
            'clear': clear,
            'data': {'x': x,
                     'y': y,
                     'r': r,
                     'fill': fill,
                     'color': color,
            },}

def make_line(x1, y1, x2, y2, clear=False, color='black'):
        return  {'type': 'line',
                 'clear': clear,
                 'data': {'x1': x1,
                          'y1': y1,
                          'x2': x2,
                          'y2': y2,
                          'color': color,
                 },}

def make_path(path, clear=False, fill=False, color='black'):
    return {'type': 'path',
            'clear': clear,
            'data': {'path': path,
                     'fill': fill,
                     'color': color,
            },}


def make_dot(x, y, color='black', clear=False):
    return make_rect(x, y, 1, 1, fill=True, color=color, clear=clear)

def make_clear(clear_rect=None):
    return {'type': 'clear',
            'clear-rect': clear_rect,
            'clear': True,}
