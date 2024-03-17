import random



def prime_checker(p):
    # Checks If the number entered is a Prime Number or not
    if p < 1:
        return -1
    elif p > 1:
        if p == 2:
            return 1
        for i in range(2, p):
            if p % i == 0:
                return -1
            return 1

def get_result(message):
    index = message.find("b:") + 2
    return int(message[index:])

def primitive_check(g, p, L):
    # Checks If The Entered Number Is A Primitive Root Or Not
    for i in range(1, p):
        L.append(pow(g, i) % p)
    for i in range(1, p):
        if L.count(i) > 1:
            L.clear()
            return -1
    return 1

def get_P(): #getting P
    P = generate_random_p()
    return P

def get_G(P): #getting G
    l = []
    while 1:
        G = random.random()
        if primitive_check(G, P, l) == -1:
            print(f"Number Is Not A Primitive Root Of {P}, Please Try Again!")
            continue
        return G


def is_prime(n):
    if n <= 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

def generate_random_p():
    while True:
        random_number = random.randint(2, 10**6)  # Adjust the range as needed
        if is_prime(random_number):
            return random_number


def get_a(P):
    a = random.random() * P
    return a

def get_result(message):
    index = message.find("b:") + 2
    return int(message[index:])

def get_P_G(message,pg):
     index = message.find(pg) + 2
     message = message[index:]
     index = message.find(",")
     return int(message[:index])

