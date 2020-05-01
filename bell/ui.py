from bell.consts import SCREEN_HEIGHT, SCREEN_WIDTH
import math

def prefix_api_resource_url(uri):
    return 'http://localhost:5000/' + uri

def make_text(content, x, y, clear=False, max_width=SCREEN_WIDTH, color='white', font_size=12):
    return {'type': 'text-msg',
            'clear': clear,
            'data': {'content': content,
                     'x': x,
                     'y': y,
                     'max-width': max_width,
                     'color': color,
                     'font-size': font_size,
            },}

def make_rect(x, y, w, h, r=0, clear=False, fill=False, color='white'):
    return {'type': 'rect',
            'clear': clear,
            'data': {'x': x,
                     'y': y,
                     'w': w,
                     'h': h,
                     'r': r,
                     'fill': fill,
                     'color': color,
            },}

def make_ellipse(x, y, rx, ry, rotation=0, start_angle=0, end_angle=math.pi*2, clear=False, fill=False, color='white'):
    return {'type': 'ellipse',
            'clear': clear,
            'data': {'x': x,
                     'y': y,
                     'rx': rx,
                     'ry': ry,
                     'rotation': rotation,
                     'start-angle': start_angle,
                     'end-angle': end_angle,
                     'fill': fill,
                     'color': color,
            },}


def make_circle(x, y, r, clear=False, fill=False, color='white'):
    return {'type': 'circle',
            'clear': clear,
            'data': {'x': x,
                     'y': y,
                     'r': r,
                     'fill': fill,
                     'color': color,
            },}

def make_line(x1, y1, x2, y2, clear=False, color='white'):
        return  {'type': 'line',
                 'clear': clear,
                 'data': {'x1': x1,
                          'y1': y1,
                          'x2': x2,
                          'y2': y2,
                          'color': color,
                 },}

def make_path(path, clear=False, fill=False, color='white'):
    return {'type': 'path',
            'clear': clear,
            'data': {'path': path,
                     'fill': fill,
                     'color': color,
            },}

def make_image(src, x, y, w, h, clear=False):
    return {'type': 'image',
            'clear': clear,
            'data': {'x': x,
                     'y': y,
                     'w': w,
                     'h': h,
                     'src': prefix_api_resource_url(src),
            },}

def make_animation(src, x, y, w, h):
    return {'type': 'gif',
            'clear': True,
            'data': {'x': x,
                     'y': y,
                     'w': w,
                     'h': h,
                     'src': prefix_api_resource_url(src),
            }}


def make_dot(x, y, color='white', clear=False):
    return make_rect(x, y, 1, 1, fill=True, color=color, clear=clear)

def make_clear(clear_rect=None):
    return {'type': 'clear',
            'clear-rect': clear_rect,
            'clear': True,}
