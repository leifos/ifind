class EnchantTokenizer(object):
    _SINGLETON_TOKENIZER = None

    def __call__(self, query):
        if EnchantTokenizer._SINGLETON_TOKENIZER is None:
            from enchant.tokenize import get_tokenizer
            EnchantTokenizer._SINGLETON_TOKENIZER = get_tokenizer('en_US')
            # XXX make language configurable

        return EnchantTokenizer._SINGLETON_TOKENIZER(query)


if __name__ == '__main__':
    e = EnchantTokenizer()
    print e('hello world')
