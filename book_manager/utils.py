def get_random_name(length=11):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters) for i in range(length))



if __name__ == '__main__':
    print(get_random_name(15))