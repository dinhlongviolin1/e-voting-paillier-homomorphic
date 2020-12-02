import os

def execute_main():
    if not os.path.isfile('encrypted_vote.txt') or not os.path.isfile('vote_status.txt'):
        print("No vote found! The election might haven't started!")
        return
    with open("vote_status.txt", "r") as reader:
        if reader.readline() == "0":
            print("Voting has not ended yet!")
            return
    c_list = []
    file = open("encrypted_vote.txt", "r")
    for x in file:
        c_list.append(int(x.strip().split(" ")[0]))
    file.close()
    with open("public.txt", "r") as reader:
        n = int(reader.readline().strip().split(" ")[0])
    total = 1
    for x in c_list:
        total *= x
    c_homomorphic = total % (n**2)
    file = open("homomorphic_vote.txt", "w")
    file.write(str(c_homomorphic))
    file.close()
    print("Data wrote to file!")
    print("Homomorphic operation succeeded! C =", str(c_homomorphic))
    

if __name__ == "__main__":
    execute_main()