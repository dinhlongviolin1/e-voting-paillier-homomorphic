# RMIT University Vietnam
# Dinh Long Nguyen - s3804737
# voting_authority.py

import os
import random

# import important config variables
from config import *

# Function Declarations

# Calculates Euclidian GCD,	return (g, x, y) ...	a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(a, m):  # Calculates Inverse Mod
    g, x, y = egcd(a, m)
    if g != 1:
        # raise Exception('modular inverse does not exist')
        return -1
    else:
        return x % m

# define a function
def lcm(x, y):
    #"""This function takes two integers and returns the L.C.M."""
    # choose the greater number
    if x > y:
        greater = x
    else:
        greater = y
    LCM = 0
    while(True):
        if((greater % x == 0) and (greater % y == 0)):
            LCM = greater
            break
        greater += 1

    return LCM

def gcd(x, y):
    """
    Calculate gcd based on lcm: gcd(x,y) = x*y/lcm(x,y) (x,y > 0)
    Reference: Wikibooks. "Greatest Common Divisor". Viewed on 2 December 2020, from https://en.wikibooks.org/wiki/Undergraduate_Mathematics/Greatest_common_divisor
    """
    return abs(x * y) / lcm(x, y)


def isPrime(n):
    """
    Reference: "isPrime python program". Viewed on 2 December 2020, from https://www.geeksforgeeks.org/python-program-to-check-whether-a-number-is-prime-or-not/
    """
    # Corner cases
    if (n <= 1):
        return False
    if (n <= 3):
        return True
    # This is checked so that we can skip
    # middle five numbers in below loop
    if (n % 2 == 0 or n % 3 == 0):
        return False
    i = 5
    while(i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0):
            return False
        i = i + 6
    return True


def generate2Prime(a=0, b=100):
    """
    Generate 2 different random prime number with lower and upper bound
    Reference: Stackoverflow. "Random Prime Number". Viewed on 2 December 2020, from https://stackoverflow.com/questions/27831283/random-prime-number-in-python
    """
    n1 = 0
    n2 = 0
    primes = [i for i in range(a, b) if isPrime(i)]
    if len(primes) >= 2:
        n1 = random.choice(primes)
        primes.remove(n1)
        n2 = random.choice(primes)
    return n1, n2

def print_candidate_result(data):
    """
    Analyze data and print final result after decryption
    """
    max_count = max(data)
    max_occurences = data.count(max_count)
    if max_occurences ==  1:
        print("Candidate " + str(data.index(max_count)+ 1) + " win this election with " + str(max_count) + " votes!")
    else:
        print("This election results in a draw between " + str(max_occurences) + " candidates, each of whom have " + str(max_count) + " votes!")

# Execute option

def generate_data():
    """
    Generate data options. Generate Paillier public and private key, setup appropriate files.
    """
    inp_test = input(
        "Do you want to test paillier encryption key? 1 for yes, other value for no: ")
    allValueFound = False
    n, g, L, k, meu, p, q = 0, 0, 0, 0, 0, 0, 0
    # Loop until all values is found
    while not allValueFound:
        # Generate p, q prime number
        p, q = generate2Prime(prime_lowerbound, prime_upperbound)
        # if the below condition is not met, these two prime number is not independant 
        # Reference: Mohamed Nassar, Qutaibah Malluhi, Tanveer Khan, "A Scheme for Three-way Secure and Verifiable E-Voting", Computer Systems and Applications (AICCSA) 2018 IEEE/ACS 15th International Conference. Accessed on 2 December 2020, from https://ieeexplore.ieee.org/document/7338149/citations#citations
        while gcd(p*q, (p-1)*(q-1)) != 1:
            # Regenerate p and q if condition is not met
            print("Regenerating p and q!")
            p, q = generate2Prime(prime_lowerbound, prime_upperbound)
        n = p*q
        # Generate random G value from range
        # Reference: Mohamed Nassar, Qutaibah Malluhi, Tanveer Khan, "A Scheme for Three-way Secure and Verifiable E-Voting", Computer Systems and Applications (AICCSA) 2018 IEEE/ACS 15th International Conference. Accessed on 2 December 2020, from https://ieeexplore.ieee.org/document/7338149/citations#citations
        g = random.randrange(1, n**2 + 1)
        L = lcm((p-1), (q-1))
        u = pow(g, L, n*n)
        k = int((u-1)/n)
        meu = int(modinv(k, n))
        if meu == -1:
            print("Redoing the generation! Modular inverse not found!")
        elif n < minimum_n_value:
            print("n is too small! Do not satisfy n >=", str(minimum_n_value),  "(larger than", str(number_of_bits* number_of_candidates) ,"bits binary)!")
        else:
            allValueFound = True
    # Write private and pulick key to file
    file_public = open("public.txt", "w")
    file_public.write(str(n) + " " + str(g))
    file_public.close()
    file_private = open("private.txt", "w")
    file_private.write(str(n) + " " + str(L) + " " + str(meu))
    file_private.close()
    print("-------------------------------------------------")
    print("Private key file and public key file is generated")
    print("-------------------------------------------------")
    # Generate voter info (name, id , has_voted, vote_id)
    file_voter = open("voter.txt", "w")
    for i in range(1, voter + 1):
        file_voter.write("Voter" + str(i) + " " + str(i) + " " + "0 -1\n")
    file_voter.close()
    print("Voter information file is generated")
    print("There are a total of " + str(voter) +
          " voters (Voter1 to Voter" + str(voter) + ")!")
    print("-------------------------------------------------")
    # Set vote_status to 0 (not finished voting)
    with open('vote_status.txt', 'w') as writer:
        writer.write("0")
    # Remove previous data encrypted file if existed
    if os.path.exists("encrypted_vote.txt"):
        os.remove("encrypted_vote.txt")
    if os.path.exists("homomorphic_vote.txt"):
        os.remove("homomorphic_vote.txt")
    print("All system file has been reinitialized!")
    print("-------------------------------------------------")
    # Print out Paillier key info
    print("The value of 'p' and 'q' is: ", str(p), ",", str(q))
    print("The value of 'n' is: "+str(n))
    print("The Public-Key (n,g) := ("+str(n)+", "+str(g)+")")
    print("The value of 'Lambda' is: "+str(L))
    print("The value of k is := "+str(k))
    print("The value of 'Meu' is := "+str(meu))
    print("Private-Key (Lambda,Meu) := ("+str(L)+", "+str(meu)+")")
    # Testing paillier key
    if inp_test == "1":
        print("-------------------- Testing --------------------")
        m_str = input(
            "Enter the value of Message 'm' (as Integer), m < " + str(n) + ": ")
        m = int(m_str)
        r_str = input("Enter the value of 'r' (as Integer): ")
        r = int(r_str)
        C = int(((g**m)*(r**n)) % (n*n))
        print("Ciphertext, C := "+str(C))
        u1 = pow(C, L, n*n)
        L_of_u1 = int((u1-1)/n)
        M = int((L_of_u1 * meu) % n)
        print("Extracted Message, M := " + str(M))


def decrypt_homomorphic():
    """
    Decrypt homomorphic encrypted data and print out election result
    """
    # Check to see if necessary files is available
    if not os.path.isfile('private.txt'):
        print("No private key found! Please run election data generation in this program!")
        return
    if not os.path.isfile('homomorphic_vote.txt'):
        print("No homomorphic encrypted data found! Please run homomorphic_server.py if voting has ended!")
        return
    # Open files to get necessary data
    with open("homomorphic_vote.txt", "r") as reader:
        c_homomorphic = int(reader.readline())
    with open("private.txt", "r") as reader:
        data = reader.readline().strip().split(" ")
        n, L, meu = int(data[0]), int(data[1]), int(data[2])
    # Decrypt Homomorphic data
    u1 = pow(c_homomorphic, L, n*n)
    L_of_u1 = int((u1-1)/n)
    M = int((L_of_u1 * meu) % n)
    # Convert message result to binary
    data_M = str(bin(M))[2:].zfill(number_of_candidates * number_of_bits)
    print("Extracted Homomorphic Message: M := " + str(M))
    print("Convert to binary:", data_M)
    # Convert vote count binary to list and reverse list for ascending candidate index
    vote_count_candidates = [int(data_M[i:i+number_of_bits], 2) for i in range(0, len(data_M), number_of_bits)][::-1]
    print("Vote count array for candidates (candidate 1 to candidate", str(number_of_candidates) + "):" ,str(vote_count_candidates))
    # Print out final results
    print_candidate_result(vote_count_candidates)

# Main function
# Run if the file is executed directly (not through import)
if __name__ == "__main__":
    print("Python File for Voting Authority")
    inp = input(
        "Enter 1 for data and paillier key generation, 2 for decrypting the homomorphic value from server for final result: ")
    if inp == "1":
        generate_data()
    elif inp == "2":
        decrypt_homomorphic()
    else:
        print("wrong input!")
