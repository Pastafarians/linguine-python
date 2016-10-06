#!/usr/bin/env python
"""
Removes all silent pause tokens, {SL}, from a text.
Returns the text as a single string separated by spaces.
"""

class RemoveSilence:
    def run(self, data):
        results = []
        for corpus in data:
            split_string = corpus.contents.split(" ")
            temp_corpus = list(filter(("{SL}").__ne__, split_string))
            temp_corpus = list(filter(("{sl}").__ne__, temp_corpus))
            corpus.contents = " ".join(temp_corpus)
            results.append(corpus)
        return results
