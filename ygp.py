#!/usr/bin/env python

cmu_stream = open('cmudict/cmudict.dict', 'r')
cmu = [line for line in cmu_stream]

cmu_dict = {}


sound_stream = open('cmudict/cmudict.phones', 'r')
sounds = [line.split('\t')[0] for line in sound_stream]


for line in cmu:
    split = line.strip().split(' ')
    if "(0)" not in split[0] and "(1)" not in split[0] and "(2)" not in split[0] and "(3)" not in split[0] and "(4)" not in split[0]:
        cmu_dict[split[0]] = ' '.join([''.join([i for i in sound if not i.isdigit()]) for sound in split[1:]])


reverse_cmu = {}
for k, v in cmu_dict.iteritems():
    reverse_cmu[v] = k


def get_phonemes(sentence):
    return ' '.join([cmu_dict[word] for word in sentence.split(' ')])


def get_similar_sound(word, distance=1):
    # sounds = "B AH T ER"
    split_word = get_phonemes(word).split(' ')
    possible_similars = set()
    for i in range(len(split_word) + 1):
        for sound in sounds:
            temp_word = split_word[:]
            temp_word.insert(i, sound)
            if distance > 1:
                new_similars = get_similar_sound(word, distance-1)
                for s in new_similars:
                    possible_similars.add(s)
            possible_similars.add(" ".join(temp_word))

    for i in range(len(split_word)):
        for sound in sounds:
            temp_word = split_word[:]
            temp_word.pop(i)
            if distance > 1:
                new_similars = get_similar_sound(word, distance-1)
                for s in new_similars:
                    possible_similars.add(s)
            possible_similars.add(" ".join(temp_word))

    for i in range(len(split_word)):
        for sound in sounds:
            temp_word = split_word[:]
            temp_word[i] = sound
            if distance > 1:
                new_similars = get_similar_sound(word, distance-1)
                for s in new_similars:
                    possible_similars.add(s)
            possible_similars.add(" ".join(temp_word))

    return possible_similars


results = set()


def get_sentences_from_sound_list(sound_list, depth=0, stack=""):
    global results
    # sound_list = ['H', 'OW', 'AA', 'R', 'Y', 'OO']

    for length in range(1, len(sound_list)):
        sound_to_check = sound_list[:length+1]
        if " ".join(sound_to_check) in reverse_cmu:
            # we found a word, recurse with sound_list[length+1:]
            # print 2 * depth * " " + reverse_cmu[" ".join(sound_to_check)]
            if len(sound_list[length+1:]) == 0:
                results.add(stack)
                return
            get_sentences_from_sound_list(sound_list[length+1:], depth+1, stack = stack + " " + reverse_cmu[" ".join(sound_to_check)])



similar_sounds = get_similar_sound("i made my family disappear" + " a", 2)

# print(list(similar_sounds)[:5])

for i in range(len(list(similar_sounds))):
    get_sentences_from_sound_list(list(similar_sounds)[i].split(' '))

for i in list(results):
    print i
