# coding:utf-8
from collections import Counter
import math


def read_file(fname):
    word_list = []
    for line in open(fname).read().split("\n"):
        word_list.extend(line.split(" "))

    wlist = Counter(word_list)
    word_ct_dict = dict(wlist.most_common(300000))
    total_ct = float(sum(map(lambda i: i[1], word_ct_dict.items())))
    word_prob_dict = {}
    for word in word_ct_dict.keys():
        word_prob_dict[word] = word_ct_dict[word] / total_ct
    return word_prob_dict, total_ct


def classify_test(economy_prob_dict, politics_prob_dict, \
                  test_economy_fname, test_politics_fname,
                  economy_prob, politics_prob):
    def decision(line):
        # each_economy_prob = math.log(economy_prob)
        # each_politics_prob = math.log(politics_prob)
        each_economy_prob = 0
        each_politics_prob = 0
        for word in line.split(" "):
            if word not in economy_prob_dict or word not in  politics_prob_dict:
                continue
            each_economy_prob += math.log((economy_prob_dict.get(word, 0))/economy_prob)
            each_politics_prob += math.log((politics_prob_dict.get(word, 0))/politics_prob)
        if each_economy_prob > each_politics_prob:
            return "economy"
        else:
            return "politics"

    economy_correct_ct = 0
    economy_total_ct = 0
    for line in open(test_economy_fname).read().split("\n"):
        result = decision(line)
        if result == 'economy':
            economy_correct_ct += 1
        economy_total_ct += 1
    print "economy precision:",economy_correct_ct / float(economy_total_ct)

    politics_correct_ct = 0
    politics_total_ct = 0
    for line in open(test_politics_fname).read().split("\n"):
        result = decision(line)
        if result == 'politics':
            politics_correct_ct += 1
        politics_total_ct += 1
    print "politics precision:",politics_correct_ct / float(politics_total_ct)


if __name__ == "__main__":
    import os

    dir = os.path.expanduser('~') + "/workspace/naive_bayesian_classifer/"
    economy_fname = dir + 'train/economy/economy.txt'
    politics_fname = dir + 'train/politics/politics.txt'
    economy_prob_dict, economy_total_ct = read_file(fname=economy_fname)
    politics_prob_dict, politics_total_ct = read_file(fname=politics_fname)

    economy_prob = economy_total_ct / float(economy_total_ct + politics_total_ct)
    politics_prob = politics_total_ct / float(economy_total_ct + politics_total_ct)

    test_economy_fname = dir + 'test/economy/economy.txt'
    test_politics_fname = dir + 'test/politics/politics.txt'
    classify_test(economy_prob_dict, politics_prob_dict, \
                  test_economy_fname, test_politics_fname, economy_prob, politics_prob)

