# Assume input array has array size 3
def sum_until_negative(numbers):
    total = 0
    i = 0
    while i < len(numbers) and numbers[i] >= 0:
        total += numbers[i]
        i += 1
    return total


def test_sum_until_negative():
    assert sum_until_negative([]) == 0
    assert sum_until_negative([1,2,3]) == 6
    assert sum_until_negative([1,-3,4]) == 1
    assert sum_until_negative([-1]) == 0
    print("All tests passed")

test_sum_until_negative()