from game import format_text_width

s = format_text_width('hello world',6)
print s

s = format_text_width('hello world this is my home',8)
print s

s = format_text_width('hello world this is a really reallylongword',15)
print s
