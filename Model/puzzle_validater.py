from math import sqrt


def get_inv_count(arr):
    inv_count = 0
    number_tiles = len(arr)
    for i in range(number_tiles - 1):
        for j in range(i + 1, number_tiles):
            # count pairs(arr[i], arr[j]) such that
            # i < j and arr[i] > arr[j]
            if arr[i] != number_tiles and arr[j] != number_tiles and arr[i] > arr[j]:
                inv_count += 1

    return inv_count


# This function returns true if given
# instance of N*N - 1 puzzle is solvable
def is_solvable(puzzle):
    length = int(sqrt(len(puzzle)))

    # Count inversions in given puzzle
    inv_count = get_inv_count(puzzle)

    # If grid is odd, return true if inversion
    # count is even.
    if length & 1:
        return inv_count % 2 == 0

    else:  # grid is even
        pos = length - puzzle.index(len(puzzle)) // length
        if pos & 1:
            return inv_count % 2 == 0
        else:
            return inv_count % 2 != 0


if __name__ == '__main__':

    puzzle1 = [
        7, 11, 4, 14,
        5, 16, 9, 15,
        8, 13, 6, 3,
        12, 1, 10, 2]
    print(puzzle1)
    print(is_solvable(puzzle1) is True)

    puzzle2 = [
        13, 2, 10, 3,
        1, 12, 8, 4,
        5, 16, 9, 6,
        15, 14, 11, 7]
    print(puzzle2)
    print("expect true")
    print(is_solvable(puzzle2) is True)

    puzzle3 = [
        3, 9, 1, 15,
        14, 11, 4, 6,
        13, 16, 10, 12,
        2, 7, 8, 5]
    print(puzzle3)
    print("expect false")
    print(is_solvable(puzzle3) is True)

    puzzle4 = [
        1, 8, 2,
        9, 4, 3,
        7, 6, 5]
    print(puzzle4)
    print("expect true")
    print(is_solvable(puzzle4) is True)

    puzzle5 = [
        2, 1, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12,
        13, 14, 15, 16]
    print(puzzle5)
    print(is_solvable(puzzle5) is True)