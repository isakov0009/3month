# a = int(input('Введите число от одного до 1 до 100'))
# if a < 10:
#     print('Ваше число меньше 10')
# elif a < 20:
#     print('Ваше число меньше двадцатки')
# elif a < 30:
#     print('30 - это потолок')
# elif a < 40:
#     print('Ваше число меньше 40')
# elif a < 50:
#     print('Много, но не больше полтинника')
# elif a < 60:
#     print('Число меньше, чем шесть*десять')
# elif a < 70:
#     print('Ваше число расположено в восьмом десятке')
# elif a < 80:
#     print('Ваше число меньше 80')
# elif a < 90:
#     print('Ваше число находится в 9 десятке')
# elif a < 100:
#     print('Сотня больше вашего числа')
# else:
#     print('Хитро, но меня не обманеш, число слишком большое')

#  Два числа выбираются случайным образом (координаты клетки шахматного поля, от 1 до 8)
#  Вывести YES, если клетка белая, и NO, если клетка черная
# from random import randint
# a = randint(3,9)
# b = randint(3,9)
# print(a, b)
# if (a + b) % 2 == 1:
#     print('YES')
# else:
#     print('NO')

# y = int(input('Введите координату y: '))
# x = int(input('Введите координату x: '))
# if (y + x) % 2 == 1:
#     print('YES')
# else:
#     print('NO

# Четыре числа выбираются случайным образом (координаты клетки шахматного поля, от 1 до 8)
# Вывести YES, если ладья может сходить с первой клетки на вторую, и NO, если не может
# Напомню, что ладья ходит так:
# Л —---X
# |
# |
# |
# X
# from random import randint
# x1 = randint(1, 8)
# x2 = randint(1, 8)
# y1 = randint(1, 8)
# y2 = randint(1, 8)
# print(x1, y1)
# print(x2, y2)
# if x1 == x2 and y1 != y2 or x1 != x2 and y1 == y2:
#     print('YES')
# else:
#     print('NO')


# str_one = 'Hello. l\'m tariel'
# print(str_one)

# str_two = "hello world. l'm tariel"
# print(str_two)


# str_eroos = """hello. l'm tariel.\nMy language python"""
# print(str_eroos)

# name = "tariel"
# surname = "ssalaiev"
# print(surname + " " + name)
# print("fjgytfyguhj,", name, surname)


# name = input("bvz:")
# surname = input("famila")
# print("dfghj,", name, surname)

num1 = 222
num2 = 111
if num1 > num2:
    print(f"{num1}  {num2}")
