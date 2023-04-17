PICS = {
    1: 'krossi.jpg'
}


def get_pic_by_id(id_):
    try:
        return f'../static/img/{PICS[id_]}'
    except (IndexError, TypeError):
        return ''
