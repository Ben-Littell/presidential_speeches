import statistics as stats
import matplotlib.pyplot as plt
import math


def open_file(filename):
    real_dict = {}
    key = 'start'
    new_dict = {}
    with open(filename) as file:
        text = file.read()
        s_text = text.split('$')
        for item in s_text[1:]:
            speech = ''
            new_list = []
            s_item = item.split()
            for j in s_item:
                new_list.append(j)
            new_dict.update({f'{new_list[0]}{new_list[1]}{new_list[2]}': [{'Speech': new_list[4:]},
                                                                          {'Length': len(new_list[4:])},
                                                                          {'Date': new_list[3]},
                                                                          {'Uncut': str(new_list[4:])}]})

    return new_dict


def plot_data(title, x1, y1, y_label, x_label, plot_code1='-b*'):
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.plot(x1, y1, plot_code1)


def sentence_len(text):
    new_dict = {}
    punc_list = ['.', '!', '?', ':']
    for val in text:
        speech2 = text[val][0]['Speech']
        w_counter = 0
        len_list = []
        for item in speech2:
            w_counter += 1
            for char in item:
                if char in punc_list:
                    len_list.append(w_counter)
                    w_counter = 0
        new_dict.update({text[val][2]['Date']: stats.mean(len_list)})

    return new_dict


def gaussian_calculation(mean, standard_dev, variance):
    y_list = []
    x_list = []
    x_start = mean - 1.5 * standard_dev
    delta_x = (3 * standard_dev) / 100
    m_s = mean - standard_dev
    mps = mean + standard_dev
    for i in range(100):
        x = i * delta_x + x_start
        y = (1 / (standard_dev * math.sqrt(2 * math.pi))) * math.e ** - (((x - mean) ** 2) / (2 * variance))
        y_list.append(y)
        x_list.append(x)

        y_left = (1 / (standard_dev * math.sqrt(2 * math.pi))) * math.e ** - (((m_s - mean) ** 2) / (2 * variance))
        Left = y_left

        y_right = (1 / (standard_dev * math.sqrt(2 * math.pi))) * math.e ** - (((mps - mean) ** 2) / (2 * variance))
        Right = y_right

    plt.axis([mean - (1.5 * standard_dev), mean + (1.5 * standard_dev), min(y_list), max(y_list)])
    apex = max(y_list)
    plt.plot(x_list, y_list, '-b')
    plt.plot([mean, mean], [0, apex], '-r')
    plt.plot([mean - standard_dev, mean - standard_dev], [0, Left], '-r')
    plt.plot([mean + standard_dev, mean + standard_dev], [0, Right], '-r')
    plt.show()


def grade_level(speech, ave_sen):
    grade_list = []
    sw_ave_list = []
    vowel_list = ['A', 'E', 'I', 'O', 'U']
    dps = ['au', 'oy', 'oo']
    tps = 'iou'
    constants = \
        ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S,' 'T', 'V', 'W,' 'X', 'Y', 'Z']
    speech_counter = -1
    for val in speech:
        speech_counter += 1
        speech2 = text[val][0]['Speech']
        clean_list = []
        syllable_counter = 0
        for word in speech2:
            new_word = ''
            for char in word:
                if char.isalpha():
                    new_word += char
            clean_list.append(new_word)
        for word in clean_list:
            if len(word) > 0:
                for char in word:
                    if char.capitalize() in vowel_list:
                        syllable_counter += 1
                if word[-1].capitalize() == 'E':
                    syllable_counter -= 1
                for j in dps:
                    if j in word:
                        syllable_counter -= 1
                if tps in word:
                    syllable_counter -= 1
                if len(word) > 3:
                    if word[-3:].lower() == 'les' and word[-4].capitalize() in constants:
                        syllable_counter += 1
                if len(word) > 2:
                    if word[-2:].lower() == 'le' and word[-3].capitalize() in constants:
                        syllable_counter += 1
                if word.lower() == 'the':
                    syllable_counter += 1
        ave_sw = syllable_counter / len(speech2)
        sw_ave_list.append(ave_sw)
        grade = 0.39*ave_sen[speech_counter]+11.8*ave_sw-15.59
        grade_list.append(grade)
    return grade_list, sw_ave_list


text = open_file('Inaugural_addresses.txt')
length_list = []
date_list = []
for val in text:
    length_list.append(int(text[val][1]['Length']))
    date_list.append(int(text[val][2]['Date']))

# for item in date_list:
#     print(type(item))

length_mean = stats.mean(length_list)
length_variance = stats.variance(length_list)
length_deviation = stats.stdev(length_list)

plot_data('Speech Length', date_list, length_list, 'Speech Length', 'Dates')
plt.axhline(stats.mean(length_list))
plt.axhline(stats.mean(length_list) + stats.stdev(length_list))
plt.axhline(stats.mean(length_list) - stats.stdev(length_list))
plt.show()

gaussian_calculation(length_mean, length_deviation, length_variance)


def greater_8(text):
    new_dict = {}
    for val in text:
        speech = text[val][0]['Speech']
        w_counter = 0
        for item in speech:
            counter = 0
            for char in item:
                if char.isalpha():
                    counter += 1
            if counter >= 8:
                w_counter += 1
        new_dict[text[val][2]['Date']] = w_counter / len(speech)
    return new_dict


word_ave_dict = greater_8(text)
word_ave = [word_ave_dict[item] for item in word_ave_dict]

plot_data('% word len >= 8', date_list, word_ave, 'Percent', 'Dates')
plt.axhline(stats.mean(word_ave))
plt.axhline(stats.mean(word_ave) + stats.stdev(word_ave))
plt.axhline(stats.mean(word_ave) - stats.stdev(word_ave))
plt.show()

sentence_len_dict = sentence_len(text)
sen_ave = [sentence_len_dict[item] for item in sentence_len_dict]

plot_data('Average Sentence Length', date_list, sen_ave, 'Average Length', 'Dates')
plt.show()

# print(text['GEORGEWASHINGTON1'][0]['Speech'])

grades, syllable_ave = grade_level(text, sen_ave)

plt.subplot(3, 1, 1)
plt.plot(date_list, sen_ave, '-b*')
plt.title('Sentence Averages')
plt.ylabel('Sentence Averages')
plt.subplot(3, 1, 2)
plt.plot(date_list, syllable_ave, '-b*')
plt.title('Average Syllables')
plt.ylabel('Syllable Averages')
plt.subplot(3, 1, 3)
plt.plot(date_list, grades, '-b*')
plt.title('Grade Level')
plt.ylabel('Grade Averages')
plt.xlabel('Dates')
plt.show()
