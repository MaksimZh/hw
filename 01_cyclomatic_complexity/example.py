def foo(a, b, c, d):
    if a % 2 == 0 and  b % 2 == 0 and c % 2 == 0 and d % 2 == 0:
        return 'Все числа четные'
    elif a % 2 != 0 and  b % 2 == 0 and c % 2 == 0 and d % 2 == 0:
        return 'Все числа четные, кроме числа А'
    elif a % 2 == 0 and  b % 2 != 0 and c % 2 == 0 and d % 2 == 0:
        return 'Все числа четные, кроме числа B'
    elif a % 2 == 0 and  b % 2 == 0 and c % 2 != 0 and d % 2 == 0:
        return 'Все числа четные, кроме числа C'
    elif a % 2 == 0 and  b % 2 == 0 and c % 2 == 0 and d % 2 != 0:
        return 'Все числа четные, кроме числа D'
    elif a % 2 != 0 and  b % 2 != 0 and c % 2 == 0 and d % 2 == 0:
        return 'Числа C и D четные, а А и B нет'
    elif a % 2 != 0 and  b % 2 == 0 and c % 2 != 0 and d % 2 == 0:
        return 'Числа B и D четные, а А и C нет'
    elif a % 2 != 0 and  b % 2 == 0 and c % 2 == 0 and d % 2 != 0:
        return 'Числа B и C четные, а А и D нет'
    elif a % 2 == 0 and  b % 2 != 0 and c % 2 != 0 and d % 2 == 0:
        return 'Числа A и D четные, а B и C нет'
    elif a % 2 == 0 and  b % 2 == 0 and c % 2 != 0 and d % 2 != 0:
        return 'Числа A и B четные, а C и D нет'
    elif a % 2 == 0 and  b % 2 != 0 and c % 2 == 0 and d % 2 != 0:
        return 'Числа A и C четные, а B и D нет'
    elif a % 2 == 0 and  b % 2 != 0 and c % 2 != 0 and d % 2 != 0:
        return 'Все числа нечетные, кроме числа А'
    elif a % 2 != 0 and  b % 2 == 0 and c % 2 != 0 and d % 2 != 0:
        return 'Все числа нечетные, кроме числа B'
    elif a % 2 != 0 and  b % 2 != 0 and c % 2 == 0 and d % 2 != 0:
        return 'Все числа нечетные, кроме числа C'
    elif a % 2 != 0 and  b % 2 != 0 and c % 2 != 0 and d % 2 == 0:
        return 'Все числа нечетные, кроме числа D'
    else:
        return 'Все числа нечетные'

assert(foo(2, 4, 6, 8) == 'Все числа четные')
assert(foo(3, 4, 6, 8) == 'Все числа четные, кроме числа А')
assert(foo(2, 5, 6, 8) == 'Все числа четные, кроме числа B')
assert(foo(2, 4, 7, 8) == 'Все числа четные, кроме числа C')
assert(foo(2, 4, 6, 9) == 'Все числа четные, кроме числа D')
assert(foo(3, 5, 6, 8) == 'Числа C и D четные, а А и B нет')
assert(foo(3, 4, 7, 8) == 'Числа B и D четные, а А и C нет')
assert(foo(3, 4, 6, 9) == 'Числа B и C четные, а А и D нет')
assert(foo(2, 5, 7, 8) == 'Числа A и D четные, а B и C нет')
assert(foo(2, 4, 7, 9) == 'Числа A и B четные, а C и D нет')
assert(foo(2, 5, 6, 9) == 'Числа A и C четные, а B и D нет')
assert(foo(2, 5, 7, 9) == 'Все числа нечетные, кроме числа А')
assert(foo(3, 4, 7, 9) == 'Все числа нечетные, кроме числа B')
assert(foo(3, 5, 6, 9) == 'Все числа нечетные, кроме числа C')
assert(foo(3, 5, 7, 8) == 'Все числа нечетные, кроме числа D')
assert(foo(3, 5, 7, 9) == 'Все числа нечетные')
