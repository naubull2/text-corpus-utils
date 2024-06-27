import itertools


def chain_zip_reversed(*args):
    """zip to longest from right to left, cycling non-longests"""
    max_len = max(len(arg) for arg in args)  # find the longest list size
    start_indices = [
        max_len % len(arg) for arg in args
    ]  # calculate the starting index for each list

    for i in range(max_len):
        yield tuple(
            arg[(i + start_indices[j]) % len(arg)] for j, arg in enumerate(args)
        )


def chain_zip(*args):
    """zip to longest from left to right, cycling non-longests"""
    i_max = max(
        range(len(args)), key=lambda i: len(args[i])
    )  # find the list with most elements
    streams = [
        itertools.cycle(arg) if i != i_max else arg for i, arg in enumerate(args)
    ]
    return itertools.chain(zip(*streams))


if __name__ == "__main__":
    # Example usage
    a = ["<|user|>", "<|assistant|>"]
    b = ["speech1", "speech2", "speech3", "speech4", "speech5"]
    c = ["sep"]

    # when left truncating
    print(list(chain_zip_reversed(a, b, c)))
    """
    [('<|assistant|>', 'speech1', 'sep2'),
     ('<|user|>', 'speech2', 'sep'),
     ('<|assistant|>', 'speech3', 'sep2'),
     ('<|user|>', 'speech4', 'sep'),
     ('<|assistant|>', 'speech5', 'sep2')]
    """

    # when right truncating
    print(list(chain_zip(a, b, c)))
    """
    [('<|user|>', 'speech1', 'sep'),
     ('<|assistant|>', 'speech2', 'sep2'),
     ('<|user|>', 'speech3', 'sep'),
     ('<|assistant|>', 'speech4', 'sep2'),
     ('<|user|>', 'speech5', 'sep')]
    """
