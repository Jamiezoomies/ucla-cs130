def process_age(age):
    if age < 0:
        return "Invalid"
    if age < 18:
        return "Minor"
    if age > 65:
        return "Senior"
    if age < 0: # Unreachable!
        return "Error"
    return "Adult"

def test_process_age():
    assert process_age(-5) == "Invalid"
    assert process_age(10) == "Minor"
    assert process_age(70) == "Senior"
    assert process_age(32) == "Adult"
    print("All tests passed")

test_process_age()
