class Node:
    """Simple node used for the Queue structure."""
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    """FIFO queue to store final results."""
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, value):
        node = Node(value)

        if self.rear is None:
            self.front = node
            self.rear = node
        else:
            self.rear.next = node
            self.rear = node

    def dequeue(self):
        if self.front is None:
            raise IndexError("Queue is empty")

        value = self.front.value
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        return value

    def is_empty(self):
        return self.front is None


class NumberList:
    """Encapsulates input numbers and calculates required sum."""
    def __init__(self, numbers):
        self.numbers = numbers

    def __len__(self):
        return len(self.numbers)

    def sum_fourth_power_non_positive(self):
        return self._recursive_sum(0, 0)

    def _recursive_sum(self, index, accumulator):
        if index >= len(self.numbers):
            return accumulator

        value = int(self.numbers[index])

        if value <= 0:
            accumulator += value ** 4

        return self._recursive_sum(index + 1, accumulator)


def validate_case(expected_count, number_list):
    return expected_count == len(number_list)


def process_cases(total_cases, result_queue):
    if total_cases == 0:
        return

    expected_count = int(input().strip())
    values = input().split()

    numbers = NumberList(values)

    if not validate_case(expected_count, numbers):
        result_queue.enqueue(-1)
    else:
        result_queue.enqueue(numbers.sum_fourth_power_non_positive())

    return process_cases(total_cases - 1, result_queue)


def print_results(result_queue):
    if result_queue.is_empty():
        return

    print(result_queue.dequeue())
    return print_results(result_queue)


if __name__ == "__main__":
    total_cases = int(input().strip())
    results = Queue()

    process_cases(total_cases, results)
    print_results(results)
