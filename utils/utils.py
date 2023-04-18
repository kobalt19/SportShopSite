PICS = {
    1: 'krossi.jpg',
    2: 'krossi.jpg',
    3: 'krossi.jpg',
    4: 'krossi.jpg',
    5: 'krossi.jpg',
    6: 'krossi.jpg',
    7: 'krossi.jpg',
    8: 'krossi.jpg',
}


def get_pic_by_id(id_):
    try:
        return f'../static/img/{PICS[id_]}'
    except (IndexError, TypeError):
        return ''
