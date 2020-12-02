# RMIT University Vietnam
# Dinh Long Nguyen - s3804737
# config.py

# Contain neccesaary config variables for voting_authority.py and vote.py

# Upper and lower bound for Paillier p and q prime number generation, might need to change if number_of_bits or number_of_candidates change to find appropriate n = p*q value
prime_upperbound = 100
prime_lowerbound = 0

# Number of election candidates
number_of_candidates = 4

# Number of binary bits for each candidate to count vote, which directly affects the total number of voters possible
number_of_bits = 2

# calculate the minimum number for n, which determine the total possible vote for each candidates
# if number of candidates = 4 and number of bits 2 -> minimum number of n must be 256 so that there can be 2 bits binary dedicated to 4 voting candidate --> Minimum value of n in binary = 11 11 11 11 (each 2 bits for each candidates) = 256 in decimal
minimum_n_value = int(''.join([''.join(["1" for y in range(0, number_of_bits)]) for x in range(0, number_of_candidates)]), 2) + 1  # 256

# for minimum_n_value = 256, voter (number of voter) can't be larger than 3 (maximum number of votes is 3 due to number of binary dedicated to each candidate count is 2 bits (0b11). To accomodate more voter, increase the number_of_bits.
voter = 3