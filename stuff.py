import matplotlib.pyplot as plt
import math

def open_file(file_name):
    speech_dictionary = {}
    first = 0
    middle = 0
    last = 0
    term = 0
    date = 0

    row_len = 0
    speech_len = 0

    with open(file_name) as file:
        for row in file:

            row = row.split()


            if len(row) == 0:
                pass

            elif row[0] == '$' and len(row) != 1:

                speech_len = 0
                row_len = len(row) - 1

                first = row[1]

                date = int(row[-1])


                if row_len == 5:
                    middle = row[2]
                    last = row[3]
                    term = row[4]


                elif row_len == 4 and len(row[3]) == 1:
                    middle = None
                    last = row[2]
                    term = row[3]


                if row_len == 4 and len(row[3]) != 1:
                    term = None
                    middle = row[2]
                    last = row[3]


                if row_len == 3:
                    middle = None
                    term = None
                    last = row[2]

            else:
                speech_len += len(row)
                # print(speech_len)

            speech_dictionary[date] = [first, middle, last, term, speech_len]

        return speech_dictionary



# speech_dictionary = open_file('Speeches.txt')
#
#
# print(speech_dictionary)

def plot_data(speech_dictionary, mean, standard_dev):

    year_list = []
    length_list = []

    for key, value in speech_dictionary.items():

        year_list.append(key)
        length_list.append(value[-1])

    # print(year_list, length_list)


    plt.title('SPEECH VS INAUGURAL YEAR :)')

    plt.plot(year_list, length_list, '-b*')


    plt.plot([year_list[0], year_list[-1]], [mean, mean], '-r')

    plt.plot([year_list[0], year_list[-1]], [mean + standard_dev, mean + standard_dev], '-r')

    plt.plot([year_list[0], year_list[-1]], [mean - standard_dev, mean - standard_dev], '-r')



    plt.axis([year_list[0] - 10, year_list[-1] + 10, 0, max(length_list) + 100])

    plt.show()

    return length_list


def calculate_numbers(speech_dictionary, start, end):

    mean = 0
    variance = 0
    standard_dev = 0
    median = 0
    big = 0
    small = 0

    number_list = []
    date_list = []

    if start > end:
        print('ERROR START DATE IS GREATER THAN END DATE')
        return

    for key, value in speech_dictionary.items():
        length = value[-1]
        if int(key) >= start and int(key) <= end:
            # print(key, length)
            number_list.append(length)
            date_list.append(key)
    # print(number_list, date_list)

    number_list.sort()


    mean = sum(number_list) / len(date_list)
    # print(mean)

    difference_list = []

    for number in number_list:
        difference_list.append((number - mean) ** 2)


    variance = sum(difference_list) / len(date_list)
    # print(variance)

    standard_dev = math.sqrt(variance)
    # print(standard_dev)
    # print(number_list)
    if len(number_list) % 2 == 0:
        middle = int((len(number_list) / 2) - 1)
        # print(middle)
        median = (number_list[middle] + number_list[middle + 1]) / 2

    else:
        middle = int((len(number_list) + 1) / 2)
        median = number_list[middle - 1]

    # print(median)

    minimum = min(number_list)
    maximum = max(number_list)

    return mean, variance, standard_dev, median, maximum, minimum


def gaussian_calculation(number_list, mean, standard_dev, variance):
    y_list = []
    x_list = []
    x_start = mean - 1.5 * standard_dev

    delta_x = (3 * standard_dev) / 100

    number_dictionary = {}

    for i in range(100):

        x = i * delta_x + x_start


        y = ( 1/(standard_dev * math.sqrt(2*math.pi)) ) * math.e ** - ( ((x - mean)** 2) / (2 * variance) )
        y_list.append(y)
        x_list.append(x)

        number_dictionary[x] = y


    plt.axis([mean - (1.5 * standard_dev), mean + (1.5 * standard_dev), min(y_list), max(y_list)])

    apex = max(y_list)

    plt.plot(x_list, y_list, '-b')

    plt.plot([mean, mean], [0, apex], '-r')

    plt.plot([mean - standard_dev, mean - standard_dev], [0, apex], '-r')

    plt.plot([mean + standard_dev, mean + standard_dev], [0, apex], '-r')



    plt.show()

def main(filename):

    speech_dictionary = open_file(filename)

    mean, variance, standard_dev, median, maximum, minimum = calculate_numbers(speech_dictionary, 1789, 2021)
    print(f'mean: {mean}, variance: {variance}, standard_dev: {standard_dev}, median: {median}, maximum: {maximum}, minimum: {minimum}')

    number_list = plot_data(speech_dictionary, mean, standard_dev)


    #
    # mean, variance, standard_dev, median, maximum, minimum = calculate_numbers(speech_dictionary, 1936, 2021)
    # print(f'mean: {mean}, variance: {variance}, standard_dev: {standard_dev}, median: {median}, maximum: {maximum}, minimum: {minimum}')
    # print(median)

    gaussian_calculation(number_list, mean, standard_dev, variance)

main('Speeches.txt')
