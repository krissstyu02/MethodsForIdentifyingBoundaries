import cv2
import numpy as np

# реализация операции свёртки
def Convolution(img, kernel):
    kernel_size = len(kernel)
    # начальные координаты для итераций по пикселям
    x_start = kernel_size // 2
    y_start = kernel_size // 2
    # переопределение матрицы изображения для работы с каждым внутренним пикселем
    matr = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            matr[i][j] = img[i][j]
    for i in range(x_start, len(matr)-x_start):
        for j in range(y_start, len(matr[i])-y_start):
            # операция свёртки - каждый пиксель умножается на соответствующий элемент ядра свертки, а затем все произведения суммируются
            val = 0
            for k in range(-(kernel_size//2), kernel_size//2+1):
                for l in range(-(kernel_size//2), kernel_size//2+1):
                    val += img[i + k][j + l] * kernel[k +(kernel_size//2)][l + (kernel_size//2)]
            matr[i][j] = val
    return matr

# нахождение округления угла между вектором градиента и осью Х
def get_angle_number(x, y):
    tg = y/x if x != 0 else 999
    if (x < 0):
        if (y < 0):
            if (tg > 2.414):
                return 0
            elif (tg < 0.414):
                return 6
            elif (tg <= 2.414):
                return 7
        else:
            if (tg < -2.414):
                return 4
            elif (tg < -0.414):
                return 5
            elif (tg >= -0.414):
                return 6
    else:
        if (y < 0):
            if (tg < -2.414):
                return 0
            elif (tg < -0.414):
                return 1
            elif (tg >= -0.414):
                return 2
        else:
            if (tg < 0.414):
                return 2
            elif (tg < 2.414):
                return 3
            elif (tg >= 2.414):
                return 4


i = 0
def main(path, standard_deviation, kernel_size, bound_path):
    global i
    i += 1

    # Задание 1 - чтение строки полного адреса изображения и размытие Гаусса
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    imgBlur_CV2 = cv2.GaussianBlur(img, (kernel_size, kernel_size), standard_deviation)
    #cv2.imshow('Blur_Imagine', imgBlur_CV2)

    # Задание 2 - вычисление и вывод матрицы значений длин и матрицы значений углов градиентов
    # задание матриц оператора Собеля
    # Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    # Gy = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    # задание матрицы оператора Прюитта
    # Gx = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    # Gy = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]

    # задание матрицы оператора Щарра
    Gx = [[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]]
    Gy = [[-3, -10, -3], [0,   0,  0], [3,  10,  3]]

    # применение операции свёртки
    img_Gx = Convolution(img, Gx)
    img_Gy = Convolution(img, Gy)

    # переопределение матрицы изображения для работы с каждым внутренним пикселем
    matr_gradient = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            matr_gradient[i][j] = img[i][j]

    # нахождение матрицы длины вектора градиента
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            matr_gradient[i][j] = np.sqrt(img_Gx[i][j] ** 2 + img_Gy[i][j] ** 2)

    # нахождение матрицы значений углов градиента
    img_angles = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_angles[i][j] = get_angle_number(img_Gx[i][j], img_Gy[i][j])

    # вывод матрицы значений длин градиента
    img_gradient_to_print = img.copy()
    # поиск максимального значения длины градиента
    max_gradient = np.max(matr_gradient)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_gradient_to_print[i][j] = (float(matr_gradient[i][j]) / max_gradient) * 255 # необходимо для корректного отображения на экране
    #cv2.imshow('Matrix_gradient ' + str(i), img_gradient_to_print)
    #print('Матрица значений длин градиента:')
    #print(img_gradient_to_print)

    # вывод матрицы значений углов градиента
    img_angles_to_print = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_angles_to_print[i][j] = img_angles[i][j] / 7 * 255 # необходимо для корректного отображения на экране
    #cv2.imshow('Matrix_angles ' + str(i), img_angles_to_print)
    #print('Матрица значений углов градиента:')
    #print(img_angles_to_print)

    # Задание 3 - подавление немаксимумов
    # инициализация массива границ изображения
    img_border = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            angle = img_angles[i][j]
            gradient = matr_gradient[i][j]
            # проверка находится ли пиксель на границе изображения
            if (i == 0 or i == img.shape[0] - 1 or j == 0 or j == img.shape[1] - 1):
                img_border[i][j] = 0 # граничный пиксель в значении 0
            # определение смещения по осям в зависимости от значения угла градиента
            else:
                x_shift = 0
                y_shift = 0
                # смещение по оси абсцисс
                if (angle == 0 or angle == 4):
                    x_shift = 0
                elif (angle > 0 and angle < 4):
                    x_shift = 1
                else:
                    x_shift = -1
                # смещение по оси ординат
                if (angle == 2 or angle == 6):
                    y_shift = 0
                elif (angle > 2 and angle < 6):
                    y_shift = -1
                else:
                    y_shift = 1
                # проверка является ли пиксель максимальным значение градиента
                is_max = gradient >= matr_gradient[i + y_shift][j + x_shift] and gradient >= matr_gradient[i - y_shift][ j - x_shift]
                img_border[i][j] = 255 if is_max else 0
    #cv2.imshow('img_border ' + str(i), img_border)

    # Задание 4 - двойная пороговая фильтрация
    # задание пороговых границ для градиента
    lower_bound = max_gradient / bound_path
    upper_bound = max_gradient - max_gradient / bound_path
    # инициализация массива результата
    double_filtration = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            gradient = matr_gradient[i][j]
            # проверка находится ли пиксель на границы изображения
            if (img_border[i][j] == 255):
                # проверка градиента в диапазоне
                if (gradient >= lower_bound and gradient <= upper_bound):
                    flag = False
                    # проверка пикселя с максимальной длиной градиента среди соседей
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            if (flag):
                                break
                            # поиск границы
                            if (img_border[i + k][j + l] == 255 and matr_gradient[i + k][j + l] >= lower_bound):
                                flag = True
                                break
                    if (flag):
                        double_filtration[i][j] = 255
                # если значение градиента выше - верхней границы, то пиксель точно граница
                elif (gradient > upper_bound):
                    double_filtration[i][j] = 255
    cv2.imshow('Double_filtration ' + str(i), double_filtration)
    # запись в файл
    cv2.imwrite('result_pictures/shaara_test5_9.jpg', double_filtration)

    cv2.waitKey(0)


# Оператор Щарра

# main('dataset/test5.jpg',5, 5, 3)
# main('dataset/test5.jpg',5, 5, 7)
# main('dataset/test5.jpg',5, 5, 9)

# main('dataset/test5.jpg',10, 5, 3)
# main('dataset/test5.jpg',10, 5, 7)
# main('dataset/test5.jpg',10, 5, 9)

# main('dataset/test5.jpg',200, 7, 3)
# main('dataset/test5.jpg',200, 7, 7)
main('dataset/test5.jpg',200, 7, 9)


# Оператор Прюитт

# main('dataset/test5.jpg',5, 5, 3)
# main('dataset/test5.jpg',5, 5, 7)
# main('dataset/test5.jpg',5, 5, 9)

# main('dataset/test5.jpg',10, 5, 3)
# main('dataset/test5.jpg',10, 5, 7)
# main('dataset/test5.jpg',10, 5, 9)

# main('dataset/test5.jpg',200, 7, 3)
# main('dataset/test5.jpg',200, 7, 7)
# main('dataset/test5.jpg',200, 7, 9)


# Оператор Собеля

# main('dataset/test5.jpg',5, 5, 3)
# main('dataset/test5.jpg',5, 5, 7)
# main('dataset/test5.jpg',5, 5, 9)

# main('dataset/test5.jpg',10, 5, 3)
# main('dataset/test5.jpg',10, 5, 7)
# main('dataset/test5.jpg',10, 5, 9)

# main('dataset/test5.jpg',200, 7, 3)
# main('dataset/test5.jpg',200, 7, 7)
# main('dataset/test5.jpg',200, 7, 9)



