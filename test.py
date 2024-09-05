from openai import OpenAI
import random
from typing import List, Optional
import sys

client = OpenAI()


class MegaInteger():
    def __init__(
        self,
        *,
        from_num: Optional[int] = None,
        from_str_list: Optional[List[str]] = None,
        from_string: Optional[str] = None
    ):
        if from_num:
            self.integer = from_num
        elif from_str_list:
            self.integer = int(''.join(from_str_list))
        elif from_string:
            self.integer = int(from_string.replace(",", ""))
        else:
            raise Exception

    @property
    def string(self):
        return str(self.integer)

    @property
    def formatted_string(self):
        """Helper function to format a string number with commas separating every 3 digits."""
        return "{:,}".format(self.integer)

    def __add__(self, other):
        """Override the + operator to add another integer or MegaInteger."""
        if isinstance(other, MegaInteger):
            result = self.integer + other.integer
        elif isinstance(other, int):
            result = self.integer + other
        else:
            raise TypeError("Operand must be an integer or MegaInteger")
        return MegaInteger(from_num=result)


def generate_mega_integers(num_digits):
    digits_a = []
    digits_b = []

    for _ in range(num_digits):
        # Randomly select a digit for the first number
        a_digit = random.randint(0, 4)

        # For the second number, ensure the sum of digits won't cause a carry
        b_digit = random.randint(0, 4)

        digits_a.append(str(a_digit))
        digits_b.append(str(b_digit))

    # Convert the lists of digits to integers
    a = MegaInteger(from_str_list=digits_a)
    b = MegaInteger(from_str_list=digits_b)

    # Return the two integers and their sum, formatted with commas
    return a, b, a+b


standard_prompt = (
    """
    You are performing basic arithmetic. The user will supply an arithmetic problem.
    You are to return exactly only the solution to the problem, and nothing else.
    DO NOT return scientific notation. Return integers only, comma-formatted.
    """
)


def create_completion(arithmetic_string: str):
    return client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        # set this as desired
        temperature=0,
        messages=[
            {
                "role": "system", "content": standard_prompt
            },
            {
                "role": "user",
                "content": arithmetic_string
            }
        ]
    )


def generate_test_string(a: str, b: str, completion: str) -> str:
    """Generate the test_string with '1' for correct digit sums, '0' for incorrect, no carry allowed."""

    # Ensure that the lengths of a, b, and completion are the same
    assert len(a) == len(b) and len(a) == len(completion)

    test_string = []

    for i in range(len(a)):
        a_digit = int(a[i])
        b_digit = int(b[i])
        completion_digit = int(completion[i])

        # Check if the sum of the two digits is <= 9 and matches the completion digit
        if a_digit + b_digit <= 9 and (a_digit + b_digit) == completion_digit:
            test_string.append('1')
        else:
            test_string.append('0')

    return ''.join(test_string)


def experiment(num_digits: int, repetitions: int):
    with open(f"results_{num_digits}_{repetitions}.txt", "w") as f:
        for repetition in range(repetitions):
            print("Making Mega Integers")
            a, b, sum_ab = generate_mega_integers(num_digits)

            sequence_string = f"{a.formatted_string} + {b.formatted_string}"
            print("Calling OpenAI")
            completion = MegaInteger(from_string=create_completion(sequence_string).choices[0].message.content.strip())
            print("Returning")

            # Pad all strings to the same length
            max_len = max(len(a.string), len(b.string), len(completion.string))
            a_padded = a.string.rjust(max_len, '0')
            b_padded = b.string.rjust(max_len, '0')
            completion_padded = completion.string.rjust(max_len, '0')

            # Get test_string
            test_string = generate_test_string(a_padded, b_padded, completion_padded)
            test_string = test_string.rjust(max_len)

            # Write to file
            f.write(a_padded + "\n")
            f.write(b_padded + "\n")
            f.write(completion_padded + "\n")
            f.write(test_string + "\n")
        f.write("\n")


experiment(int(sys.argv[1]), 1)