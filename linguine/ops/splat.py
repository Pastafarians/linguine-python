#!/usr/bin/env python
"""
Returns:
Given:
"""

from splat.base.TextBubble import TextBubble
import splat.base.Util as Util
from splat.parse.TreeStringParser import TreeStringParser
import json, sys

class SplatDisfluency:
    def __init__(self):
        pass
    def run(self, data):
        results = [ ]
        try:
            for corpus in data:
                temp_bubble = TextBubble(corpus.contents)
                raw_disfluencies = Util.count_disfluencies(temp_bubble.sents())
                results.append({'corpus_id': corpus.id, 'disfluencies': raw_disfluencies[0],
                                'average_disfluencies': raw_disfluencies[1]})
            results = json.dumps(results)
            print(results)
            return results
        except TypeError:
            raise TransactionException('Corpus contents does not exist.')

class SplatNGrams:
    def __init__(self):
        pass
    def run(self, data):
        results = [ ]
        try:
            for corpus in data:
                temp_bubble = TextBubble(corpus.contents)
                bigrams = temp_bubble.bigrams()
                trigrams = temp_bubble.trigrams()
                results.append({'corpus_id': corpus.id,
                                'bigrams': bigrams,
                                'trigrams': trigrams})
            results = json.dumps(results)
            print(results)
            return results
        except TypeError:
            raise TransactionException('Corpus contents does not exist.')

class SplatComplexity:
    def __init__(self):
        pass
    def run(self, data):
        results = [ ]
        try:
            for corpus in data:
                temp_bubble = TextBubble(corpus.contents)

                cdensity = temp_bubble.content_density()
                idensity = temp_bubble.idea_density()
                flesch_score = temp_bubble.flesch_readability()
                kincaid_score = temp_bubble.kincaid_grade_level()
                results.append({'corpus_id': corpus.id,
                                'content_density': cdensity,
                                'idea_density': idensity,
                                'flesch_score': flesch_score,
                                'kincaid_score': kincaid_score})
            results = json.dumps(results)
            print(results)
            return results
        except TypeError as e:
            print(e)
            raise TransactionException('Corpus contents does not exist.')
