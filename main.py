import statistics as stats
import matplotlib.pyplot as plt


def open_file(filename):
    real_dict = {}
    key = 'start'
    new_dict = {}
    with open(filename) as file:
        text = file.read()
        s_text = text.split('$ ')
        for item in s_text[1:]:
            speech = ''
            new_list = []
            s_item = item.split()
            for j in s_item:
                new_list.append(j)
            # print(item)
            new_dict.update({f'{new_list[0]}{new_list[1]}{new_list[2]}': [{'Speech': new_list[4:]},
                                                                          {'Length': len(new_list[4:])},
                                                                          {'Date': new_list[3]},
                                                                          {'Uncut': item}]})

    return new_dict


def plot_data(title, x1, y1, y_label, x_label, plot_code1='-b*'):
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.axhline(stats.mean(length_list))
    plt.axhline(stats.mean(length_list)+stats.stdev(length_list))
    plt.axhline(stats.mean(length_list)-stats.stdev(length_list))
    plt.plot(x1, y1, plot_code1)


text = open_file('Inaugural_addresses.txt')
length_list = []
date_list = []
for val in text:
    length_list.append(int(text[val][1]['Length']))
    date_list.append(int(text[val][2]['Date']))

# for item in date_list:
#     print(type(item))

length_mean = stats.mean(length_list)
length_gaussian = stats.pstdev(length_list, length_mean)
length_deviation = stats.stdev(length_list)


plot_data('Speech Length', date_list, length_list, 'Speech Length', 'Dates')
plt.show()

word_ave_dict = {}
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
    word_ave_dict[text[val][2]['Date']] = w_counter/len(speech)


print(word_ave_dict)







