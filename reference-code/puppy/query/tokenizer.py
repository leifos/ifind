class BasicTokenizer(object):
    def __call__(self, query):
        return query.split()


class PunctuationAwareTokenizer(object):
    PUNCTUATION = set(' ,!.;:\'"?')

    def __call__(self, query):
        return list(self._parse(query))

    def _parse(self, query):
        buffer = []

        for c in query:
            if c in PunctuationAwareTokenizer.PUNCTUATION:
                if buffer:
                    yield ''.join(buffer)
                buffer = []
            else:
                buffer.append(c)

        if buffer:
            yield ''.join(buffer)


if __name__ == '__main__':
    p = PunctuationAwareTokenizer()

    assert p('hello world') == ['hello', 'world']
    assert p('hello, world') == ['hello', 'world']
    assert p('hello!world') == ['hello', 'world']
    assert p('hello!, ?world???') == ['hello', 'world']
