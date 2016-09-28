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
                sentences = { }
                average_disfluencies = 0
                um_count, uh_count, ah_count, er_count, hm_count, sl_count, rep_count, brk_count = (0,) * 8
                # Sort the data so it looks better in JSON
                for i in raw_disfluencies[0]:
                    temp_dis = {"UM": raw_disfluencies[0][i][0], "UH": raw_disfluencies[0][i][1], "AH": raw_disfluencies[0][i][2],
                                "ER": raw_disfluencies[0][i][3], "HM": raw_disfluencies[0][i][4], "SILENT PAUSE": raw_disfluencies[0][i][5],
                                "REPETITION": raw_disfluencies[0][i][6], "BREAK": raw_disfluencies[0][i][7]}
                    sentences[i] = temp_dis
                    for (k, v) in temp_dis.items():
                        # Gather total disfluencies for each disfluency type
                        average_disfluencies += v
                        if k == "UM": um_count += v
                        elif k == "UH": uh_count += v
                        elif k == "AH": ah_count += v
                        elif k == "ER": er_count += v
                        elif k == "HM": hm_count += v
                        elif k == "SILENT PAUSE": sl_count += v
                        elif k == "REPETITION": rep_count += v
                        elif k == "BREAK": brk_count += v

                temp_total = average_disfluencies

                # Calculate the average disfluencies per sentence in the whole text
                average_disfluencies = float(average_disfluencies / len(raw_disfluencies[0]))

                total_disfluencies = {"UM": um_count, "UH": uh_count, "AH": ah_count, "ER": er_count, "HM": hm_count,
                                      "SILENT PAUSE": sl_count, "REPETITION": rep_count, "BREAK": brk_count, "TOTAL": temp_total}

                results.append({'corpus_id': corpus.id,
                                'sentences': sentences,
                                'average_disfluencies_per_sentence': average_disfluencies,
                                'total_disfluencies': total_disfluencies})
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
                unigrams = temp_bubble.unigrams()
                bigrams = temp_bubble.bigrams()
                trigrams = temp_bubble.trigrams()
                results.append({'corpus_id': corpus.id,
                                'unigrams': unigrams,
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

class SplatPOSFrequencies:
    def __init__(self):
        pass
    def run(self,data):
        results = [ ]
        pos_parsed = {}
        try:
            for corpus in data:
                temp_bubble = TextBubble(corpus.contents)
                pos_tags = temp_bubble.pos()
                pos_counts = temp_bubble.pos_counts()
                for tuple in pos_tags:
                    k = tuple[0]
                    v = tuple[1]
                    if v in pos_parsed.keys():
                        if k not in pos_parsed[v]:
                            pos_parsed[v].append(k)
                    else:
                        pos_parsed[v] = [ ]
                        pos_parsed[v].append(k)

                results.append({'corpus_id': corpus.id,
                                'pos_tags': pos_parsed,
                                'pos_counts': pos_counts})

            results = json.dumps(results)
            print(results)
            return results
        except TypeError as e:
            print(e)
            raise TransactionExceptions('Failed to run SplatPOSFrequencies.')
