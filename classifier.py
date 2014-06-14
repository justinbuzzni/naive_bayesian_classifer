from math import log


def load_data(file_name):
    with open(file_name) as fin:
        for line in fin:
            for word in parse_line(line):
                yield word


def parse_line(line):
    # TODO: Discard non-words (e.g., puntuations, special symbols, etc.)
    return line.split()


def build_stats(words):
    word_counts = count_words(words)
    n = sum(map(lambda i : i[1],word_counts.items()))
    stats = {}
    for w, c in word_counts.items():
        # stats[w] = float(c) / n
        stats[w] = float(c)

    return stats,n


def count_words(words):
    stats = {}
    for word in words:
        stats.setdefault(word, 0)
        stats[word] += 1

    return stats


def test(file_name, economics_stats, politics_stats ,economics_prob,politics_prob, decision_function):
    """Perform test runs with test data."""

    def probability(words, stats,class_prob):
        return sum(map(lambda w: log(stats[w]/class_prob) if w in stats else 0, words))


    def probabilities():
        with open(file_name) as fin:
            for line in fin:
                words = parse_line(line)

                p1 = probability(words, economics_stats,economics_prob)
                p2 = probability(words, politics_stats,politics_prob)

                # print p1,p2
                yield decision_function(p1, p2)


    ps = list(probabilities())
    n = len(ps)
    pr = len(list(filter(lambda x: x, ps)))

    print('Precision for {} = {}/{} ({}%)'.format(
          file_name, pr, n, 100.0 * pr / n))


def class_prob(economics_word_num, politics_word_num):
    economics_prob = economics_word_num / float(economics_word_num + politics_word_num)
    politics_prob = politics_word_num / float(economics_word_num + politics_word_num)
    return economics_prob, politics_prob


def main():
    economics = load_data('train/economy/economy.txt')
    politics = load_data('train/politics/politics.txt')

    economics_stats,economics_word_num = build_stats(economics)
    politics_stats,politics_word_num = build_stats(politics)

    economics_prob, politics_prob = class_prob(economics_word_num, politics_word_num)

    test('test/economy/economy.txt',
         economics_stats, politics_stats,economics_prob,politics_prob,
         lambda x, y: x > y)
    test('test/politics/politics.txt',
         economics_stats, politics_stats,economics_prob,politics_prob,
         lambda x, y: x < y)

if __name__ == '__main__':
    main()
