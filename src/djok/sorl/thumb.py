from sorl.thumbnail import delete


def del_thumb(file_field, delete_file=True, commit=False):
    """
    Удаляет эскиз SOLR
    а так же связанный с моделью файл изображения
    :param file_field:
    :param delete_file:
    :param commit:
    :return:
    """

    if file_field:
        delete(file_field, delete_file=False)

    if delete_file:
        file_field.delete(save=commit)
