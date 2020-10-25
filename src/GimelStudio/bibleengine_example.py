from vendor import bibleengine


b = bibleengine.WordEngine()
bookfile = b.load_bible_file("Genesis")
example1 = b.get_rangeofverses_text(bookfile, 1, 1, 12)
print(example1)
