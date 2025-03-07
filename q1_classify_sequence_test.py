def classify_sequence(numbers):
    if len(numbers) == 0:
        return "Empty"
    count = 0
    i = 0
    while i < len(numbers) and i < 5: # Process at most 5 numbers
        if numbers[i] > 0:
            count += 1
        i += 1
    
    if count == 0:
        return "AllNonPositive"
    elif count == i:
        return "AllPositive"
    else:
        return "Mixed"


def test_classify_sequence():
    assert classify_sequence([])
    assert classify_sequence([1, 2, 3])
    assert classify_sequence([-1, -5, -4])
    assert classify_sequence([1, 2, -1])
    print("All tests passed")

test_classify_sequence()
    