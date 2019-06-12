def compute_rmse(list1, list2):

    list_length = len(list1)
    assert list_length == len(list2)

    compute_list = []

    # subtract
    for i in range(list_length):
        compute_list.append(list1[i] - list2[i])
    # square
    for i in range(list_length):
        compute_list[i] = compute_list[i] ** 2.
    # sum
    total = sum(compute_list)
    # divide
    total /= float(list_length)
    # root
    total = total ** 0.5

    return total
