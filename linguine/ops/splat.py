#!/usr/bin/env python
"""
Returns:
Given:
"""

from splat.base.TextBubble import TextBubble
import splat.base.Util as Util
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
                print("Calculating Content Density...")
                content_density = temp_bubble.content_density()
                print("Content Density: " + content_density)
                print("Calculating Idea Density...")
                idea_density = temp_bubble.idea_density()
                print("Idea Density: " + idea_density)
                print("Calculating Yngve Score...")
                yngve_score = temp_bubble.tree_based_yngve_score()
                print("Yngve Score: " + yngve_score)
                print("Calculating Frazier Score...")
                frazier_score = temp_bubble.tree_based_frazier_score()
                print("Frazier Score: " + frazier_score)
                results.append({'corpus_id': corpus.id,
                                'content_density': content_density,
                                'idea_density': idea_density,
                                'yngve_score': ygnve_score,
                                'frazier_score': frazier_score})
            results = json.dumps(results)
            print(results)
            return results
        except TypeError:
            raise TransactionException('Corpus contents does not exist.')
        except:
            print("Unexpected error:", sys.exc_info()[0])
