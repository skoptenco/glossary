import random, string

def random_word():
    return ''.join(random.choices(string.ascii_lowercase, k=8))