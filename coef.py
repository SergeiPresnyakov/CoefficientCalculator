import tkinter.filedialog as fd
from scipy import stats

data = {}

filename = fd.askopenfilename()

with open(filename, 'r') as file:
    for line in file:
        line = line.rstrip(';\n')
        print(line)
        row = line.split(';')
        key = row[0]

        values = row[1:]
        values = [float(x) for x in values]

        data[key] = values

# по этому ключу отделяется ряд значений Х
# он обязательно должен быть
data_x = data.pop('ВЖ ННЗ')


with open(filename[:-4] + '_coef_from_scipy.csv', 'w') as output:
    # шапка таблицы
    output.write(f'Элемент;К спирмена;к значимости;значимость;;tau Кендалла;к значимости;значимость\n')

    for key in data:
        # считаем Спирмена
        coef, p = stats.spearmanr(data_x, data[key])
        s_value = "Значимый" if abs(coef) > p else "Незначимый"

        # считаем Кендалла
        tau_kendall, kendall_p = stats.kendalltau(data_x, data[key])
        kendall_value = "Значимый" if abs(tau_kendall) > kendall_p else "Незначимый"

        # пишем в файл
        output.write(f'{key};{coef};{p};{s_value};;{tau_kendall};{kendall_p};{kendall_value}\n')
