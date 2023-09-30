import pytest
import re


def string_adder(string_input):
    try:
        if len(string_input) == 0:
            return 0

        result = 0
        delimiters_count = 0
        delimiters = [",", "\n"]
        neg_nums = []

        if string_input.startswith("//"):
            start_index = string_input.find("//")
            end_index = string_input.find("\n")

            if start_index != -1 and end_index != -1:
                new_delimiter = string_input[
                    start_index + len("//") : end_index
                ].strip()
                if "[" in string_input:
                    pattern = r"\[(.*?)\]"
                    matches = re.findall(pattern, new_delimiter)
                    delimiters = delimiters + matches
                else:
                    delimiters.append(new_delimiter)

                string_input = string_input.split("\n", 1)[1]

        for delimiter in delimiters:
            delimiters_count += string_input.count(delimiter)

        for delimiter in delimiters:
            string_input = " ".join(string_input.split(delimiter))

        nums = string_input.split()

        if string_input.endswith("\n"):
            delimiters_count -= 1

        while "" in nums:
            nums.remove("")

        if (delimiters_count + 1) != len(nums):
            raise Exception(f"The {string_input} input is not valid")
        else:
            for num in nums:
                if int(num) < 0:
                    neg_nums.append(num)

            for num in nums:
                if int(num) < 0:
                    raise Exception(f"Negatives not allowed {neg_nums}")
                if int(num) <= 1000:
                    result += int(num)
        return result

    except:
        raise Exception(f"Input {string_input} is not valid")
    finally:
        print("Operation Accomplished Successfully")

def test_simple():
    assert string_adder("") == 0
    assert string_adder("1") == 1
    assert string_adder("1,2") == 3


def test_unknown_amount_numbers():
    assert string_adder("1,2,5,6,3,8") == 25
    assert string_adder("0,2,6,12,10") == 30
    assert string_adder("1,1,1,2,2,5,80") == 92


def test_new_lines():
    assert string_adder("1\n2,3") == 6
    with pytest.raises(Exception):
        string_adder("1,\n")
    with pytest.raises(Exception):
        string_adder("\n,1,")


def test_different_delimiters():
    assert string_adder("//;\n1;2") == 3
    assert string_adder("//;\n1;2;2;4") == 9


def test_negatives_nums():
    with pytest.raises(Exception):
        string_adder("-1,-2,7,9,-6")
    with pytest.raises(Exception):
        string_adder("//;\n1;-2")


def test_large_nums():
    assert string_adder("1,2,1000") == 1003
    assert string_adder("2,1001") == 2
    assert string_adder("//;\n1;2;1234") == 3


def test_delimiters_length():
    assert string_adder("//[***]\n1***2***3") == 6
    assert string_adder("//[@#$]\n5@#$2@#$3@#$9") == 19
    assert string_adder("//[##]\n6##9##3") == 18


def test_delimiters_all():
    assert string_adder("//[**][%%%%]\n3**2%%%%3") == 8
    assert string_adder("//[#][!!][!@!]\n9#4!!3!@!5") == 21
    assert string_adder("//[*][%$%][:]\n4:2:1*3%$%5") == 15

def test_invalid_input():
    with pytest.raises(Exception):
        string_adder("/£/;2\n1;-2")
    with pytest.raises(Exception):
        string_adder("/£1,2,4")
