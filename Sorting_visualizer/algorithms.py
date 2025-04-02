def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                yield data

def quick_sort(data):
    def _quick_sort(data, low, high):
        if low < high:
            pi = partition(data, low, high)
            yield from _quick_sort(data, low, pi - 1)
            yield from _quick_sort(data, pi + 1, high)

    def partition(data, low, high):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            if data[j] < pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                yield data
        data[i + 1], data[high] = data[high], data[i + 1]
        yield data
        return i + 1

    yield from _quick_sort(data, 0, len(data) - 1)

def merge_sort(data):
    def _merge_sort(data):
        if len(data) > 1:
            mid = len(data) // 2
            left = data[:mid]
            right = data[mid:]

            yield from _merge_sort(left)
            yield from _merge_sort(right)

            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    data[k] = left[i]
                    i += 1
                else:
                    data[k] = right[j]
                    j += 1
                k += 1
                yield data

            while i < len(left):
                data[k] = left[i]
                i += 1
                k += 1
                yield data

            while j < len(right):
                data[k] = right[j]
                j += 1
                k += 1
                yield data

    yield from _merge_sort(data)

def heap_sort(data):
    def heapify(data, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and data[i] < data[left]:
            largest = left

        if right < n and data[largest] < data[right]:
            largest = right

        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            yield data
            yield from heapify(data, n, largest)

    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(data, n, i)

    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        yield data
        yield from heapify(data, i, 0)

def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
            yield data
        data[j + 1] = key
        yield data

def selection_sort(data):
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        yield data
