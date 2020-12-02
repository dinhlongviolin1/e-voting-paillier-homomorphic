# RMIT University Vietnam
# Dinh Long Nguyen - s3804737
# vote_end.py

# server code to homomorphicly combine voting data 

import os

def execute_main():
    # Check to see if neccesary files is available
    if not os.path.isfile('encrypted_vote.txt') or not os.path.isfile('vote_status.txt'):
        print("No vote found! The election might haven't started!")
        return
    # Check to see if voting process has ended
    with open("vote_status.txt", "r") as reader:
        if reader.readline() == "0":
            print("Voting has not ended yet!")
            return
    # Get all encrypted data
    c_list = []
    file = open("encrypted_vote.txt", "r")
    for x in file:
        c_list.append(int(x.strip().split(" ")[0]))
    file.close()
    # Get Paillier public key
    with open("public.txt", "r") as reader:
        n = int(reader.readline().strip().split(" ")[0])
    # Combine encrypted data through multiplication
    total = 1
    for x in c_list:
        total *= x
    # Calculate combined encryption c value
    c_homomorphic = total % (n**2)
    # Output data
    file = open("homomorphic_vote.txt", "w")
    file.write(str(c_homomorphic))
    file.close()
    print("Data wrote to file!")
    print("Homomorphic operation succeeded! C =", str(c_homomorphic))
    
# Main function
# Run if the file is executed directly (not through import)
if __name__ == "__main__":
    execute_main()