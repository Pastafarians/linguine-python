#!/usr/bin/env python
"""
Returns:
Given:
"""

from splat.base.TextBubble import TextBubble
import splat.base.Util as Util

class SplatDisfluency:
    def __init__(self):
        pass
    def run(self, data):
        results = [ ]
        try:
                for corpus in data:
                        temp_bubble = TextBubble(corpus.contents)
                        raw_disfluencies = Util.count_disfluencies(temp_bubble.sents())
                        results.append({'corpus_id': corpus.id, 'disfluencies': raw_disfluencies[0]})
                print(results)
                #return results
        except TypeError:
                raise TransactionException('Corpus contents does not exist.')
