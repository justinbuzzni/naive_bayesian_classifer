"""Will use some hard-coded values to save time."""
DOCUMENT_COUNT = 1500

from math import log


def load_data(file_name):
    with open(file_name) as fin:
        for line in fin:
            for word in parse_line(line):
                yield word


def parse_line(line):
    # TODO: Discard non-words (e.g., puntuations, special symbols, etc.)
    return set(line.split())


def build_stats(words):
    word_counts = count_words(words)
    n = DOCUMENT_COUNT
    stats = {}

    for w, c in word_counts.items():
        stats[w] = float(c) / n

    return stats


def count_words(words):
    stats = {}
    for word in words:
        stats.setdefault(word, 0)
        stats[word] += 1

    return stats


def test(file_name, economics_stats, politics_stats, decision_function):
    """Perform test runs with test data."""

    def probability(words, stats):
        return sum(map(lambda w: log(stats[w]) if w in stats else 0, words))

    def probabilities():
        with open(file_name) as fin:
            for line in fin:
                words = parse_line(line)

                p1 = probability(words, economics_stats)
                p2 = probability(words, politics_stats)

                yield decision_function(p1, p2)

    ps = list(probabilities())
    n = len(ps)
    pr = len(list(filter(lambda x: x, ps)))

    print('Precision for {} = {}/{} ({}%)'.format(
          file_name, pr, n, 100.0 * pr / n))


def main():
    economics = load_data('train/economy/economy.txt')
    politics = load_data('train/politics/politics.txt')

    economics_stats = build_stats(economics)
    politics_stats = build_stats(politics)

    test('test/economy/economy.txt',
         economics_stats, politics_stats,
         lambda x, y: x > y)
    test('test/politics/politics.txt',
         economics_stats, politics_stats,
         lambda x, y: x < y)

if __name__ == '__main__':
    main()
