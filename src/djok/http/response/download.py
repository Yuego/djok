from django_downloadview.response import (
    DownloadResponse as DownloadResponseBase,
    encode_basename_ascii,
    encode_basename_utf8,
)


def content_disposition(filename: str, attachment: bool = True) -> str:
    """Return value of ``Content-Disposition`` header with 'attachment'.

    Дополнение оригинальной функции из django_downloadview
     для поддержки явной передачи inline в заголовке

    >>> print(content_disposition('', False))
    inline

    >>> print(content_disposition('demo.txt', False))
    inline; filename="demo.txt"

    >>> print(content_disposition('demo.txt'))
    attachment; filename="demo.txt"

    If filename is empty, only "attachment" is returned.

    >>> print(content_disposition(''))
    attachment

    If filename contains non US-ASCII characters, the returned value contains
    UTF-8 encoded filename and US-ASCII fallback.

    >>> print(content_disposition(u'é.txt'))
    attachment; filename="e.txt"; filename*=UTF-8''%C3%A9.txt

    """
    disposition = 'attachment' if attachment else 'inline'

    if not filename:
        return disposition

    ascii_filename = encode_basename_ascii(filename)
    utf8_filename = encode_basename_utf8(filename)
    if ascii_filename == utf8_filename:  # ASCII only.
        return f'{disposition}; filename="{ascii_filename}"'
    else:
        return (
            f'{disposition}; filename="{ascii_filename}"; '
            f"filename*=UTF-8''{utf8_filename}"
        )


class DownloadResponse(DownloadResponseBase):
    """
    DownloadResponse, использующий обновлённую функцию content_desposition

    А так же с поддержкой установки постоянного префикса для имён файлов
    (например адреса сайта)

    """
    name_prefix: str = ''

    @property
    def default_headers(self):
        """Return dictionary of automatically-computed headers.

        Uses an internal ``_default_headers`` cache.
        Default values are computed if only cache hasn't been set.

        ``Content-Disposition`` header is encoded according to `RFC 5987
        <http://tools.ietf.org/html/rfc5987>`_. See also
        http://stackoverflow.com/questions/93551/.

        """
        try:
            return self._default_headers
        except AttributeError:
            headers = {}
            headers["Content-Type"] = self.get_content_type()
            try:
                headers["Content-Length"] = self.file.size
            except (AttributeError, NotImplementedError):
                pass  # Generated files.

            basename = self.get_basename()
            basename = f'{self.name_prefix}{basename}'

            headers["Content-Disposition"] = content_disposition(basename, self.attachment)
            self._default_headers = headers
            return self._default_headers

