# BibleEngine Copyright (C) 2018-2020 Noah Rahm, Correct Syntax. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#     3. The names of Correct Syntax, Noah Rahm and any contributers may not be
#        used to endorse or promote products derived from this software without
#        specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Originally written in 2018, so this probably needs a re-write

import os
import re


PUNCUATION = [',', ';', ':', '.', '*', '?', '!', '-',
              '&', '"', '[', ']', '(', ')', '_', '{', '}'
              ]

NUMBERS = [str(i for i in range(0, 255))]


class WordEngine(object):

    def books(self):
        """ Returns a list of the books of the Bible. """
        books = [
            'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua',
            'Judges', 'Ruth', 'I Samuel', 'II Samuel', 'I Kings', 'II Kings',
            'I Chronicles', 'II Chronicles', 'Ezra', 'Nehemiah', 'Esther',
            'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
            'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea',
            'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk',
            'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
            'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', 'I Corinthians',
            'II Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians',
            'I Thessalonians', 'II Thessalonians', 'I Timothy', 'II Timothy',
            'Titus', 'Philemon', 'Hebrews', 'James', 'I Peter', 'II Peter',
            'I John', 'II John', 'III John', 'Jude', 'Revelation'
        ]

        return books

    def clean_text(self, text, spaces=True):
        """ Cleans the input text of any puncuation and optionally, of any spaces.
        Returns a string of the text.
        ====================================
        text: The text which is to be cleaned
        spaces: Whether or not to keep the spaces.
        """
        # Append the letters in the text to a list
        text_list = []
        for word in text:
            for letter in word:
                # If the text includes puncuation, remove it
                if letter in PUNCUATION:
                    del letter

                # If the text includes numbers, remove them
                elif letter in NUMBERS:
                    del letter

                # If the character is a "\n", append a space to the list
                elif letter in ['\n']:
                    text_list.append('')

                # Append the character to the list
                else:
                    text_list.append(letter)

        # Build a string from the text list
        text_string = ""
        for letter in text_list:
            text = (text_string + letter)
            text_string = text

        # If the spaces are to be kept
        if spaces == True:
            return text_string

        # If the spaces are to be removed
        if spaces == False:
            # Take out all the spaces in the text
            text = re.findall(r'\S', text_string)

            # Rebuild the text into a string
            text_string = ""
            for letter in text:
                text = (text_string + letter)
                text_string = text

            return text_string

    def check_text(self, input_text, correct_text):
        """ Checks the input text against the correct text to see if they match
        and returns either True or False.
        ====================================
        input_text: The text which is to be compared to the correct text
        correct_text: The "correct" text to compare the "input" text to ("the standard")
        """
        # Make both texts lowercase
        input_text = (input_text.lower())
        correct_text = (correct_text.lower())

        # Remove puncuation the text
        i_text = self.clean_text(input_text, spaces=False)
        c_text = self.clean_text(correct_text, spaces=False)

        # print(i_text)
        # print(c_text)

        # If both texts are the same
        if i_text == c_text:
            return True

        # If both texts are not the same
        else:
            return False

    def get_chapter_text(self, text, chapter):
        """ Returns a string of the chapter.
        ====================================
        text: The (book) text from either a string, .txt or .bible file
        chapter: Chapter of the text to return
        """
        # Define the start and end points of the chapter
        chapter_start = text.find(('CHAPTER {}'.format(chapter)))
        chapter_end = text.find(('CHAPTER {}'.format(chapter + 1)))

        # Slice the text to get only the chapter text
        chapter_text = (text[chapter_start:chapter_end])

        return chapter_text

    def get_verse_text(self, text, chapter, verse):
        """ Returns a string of the verse.
        ====================================
        text: The (book) text from either a string, .txt or .bible file
        chapter: Chapter of the verse text to return
        verse: The verse to return from the given text and chapter
        """
        # Get the chapter text
        input_text = self.get_chapter_text(text, chapter)

        # Break the chapter text into verses
        txt = re.split("\n+", input_text)
        verse_text = txt[verse]

        return verse_text

    def get_rangeofverses_text(self, text, chapter, fromverse, toverse):
        """ Returns a string of the range of verses.
        ===============================================
        text: The (book) text from either a string, .txt or .bible file
        chapter: Chapter of the verses text to return
        fromverse: Verse number (int, NOT str) to start the range of text to return
        toverse: Verse number (int, NOT str) to end the range of text to return
        """
        # Get the chapter text
        input_text = self.get_chapter_text(text, chapter)

        # Define the start and end points of the range of verses
        section_start = input_text.find(('{}'.format(fromverse)))
        section_end = input_text.find(('{}'.format(toverse + 1)))

        # Slice the text to get only the range of verses' text
        range_of_verses_text = (input_text[section_start:section_end])

        return range_of_verses_text

    def load_bible_file(self, bookname):
        """ Opens and reads the input file. The input can only be a string of the path to
        the file and the book's name (not with the extension). This makes it simpler to
        open the desired book without having to put the ext. multiple times.
        ======================================================================
        bookname: The name of the book of the Bible as a string (e.g "the book's name")
        """
        # Get the path
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # print(BASE_DIR)
        #os.path.join(BASE_DIR, 'BibleEngine')
        bookname = ('{}/bibletexts/{}'.format(os.path.join(BASE_DIR, 'BibleEngine'), bookname))

        try:
            # If the file is .bible
            book = open("{}.bible".format(bookname), 'r').read()

        except:
            # If the file is NOT .bible, it will fallback on this
            book = open("{}.txt".format(bookname), 'r').read()

        return book


class Memorize(WordEngine):

    def compare(self, filename, input_text, chapter, fromverse, toverse):
        """ This is the main Memorization function. It compares the input text to the
        correct bible text from the module's library. It returns True if the text matches
        the correct text and False if it is incorrect.
        =================================================
        filename: The name of the book of the Bible as a string (e.g "the book's name")
        input_text: The user's text to be compared to the correct text of the Bible
        chapter: The chapter of the book of the Bible you want to memorize (filename)
        fromverse: Verse number (int, NOT str) to start the range of text to compare
        toverse: Verse number (int, NOT str) to end the range of text to compare
        """
        # Load the given book of the Bible
        bookfile = self.load_bible_file(filename)

        # Get the correct text
        correct_text = self.get_rangeofverses_text(bookfile, chapter,
                                                   fromverse, toverse)

        # Compare the texts
        result = self.check_text(input_text, correct_text)

        return result
