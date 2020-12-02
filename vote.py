import os.path
import os
import random
import copy
import vote_end
from uuid import uuid4


# number of voting candidates
candidates = 4
number_of_bits = 3


def get_public_key():
    """
    """
    file = open("public.txt", "r")
    data = file.readline().split(" ")
    n = data[0]
    g = data[1]
    print("Get public key completed!")
    return (n, g)


def get_voter():
    """
    docstring
    """
    voter = []
    file_voter = open("voter.txt", "r")
    for x in file_voter:
        data = x.strip().split(" ")
        if len(data) == 4:
            voter.append(data)
    print("Get voter information completed!")
    return voter


def get_voter_index(voter, name, id):
    """
    docstring
    """
    ans = -1
    for i in range(0, len(voter)):
        if voter[i][0] == name and voter[i][1] == id:
            ans = i
    return ans


def has_voter_vote(voter, index):
    """
    docstring
    """
    return voter[index][2] != "0"


def submit_vote(vote, vote_id, n, g, voter_arr, voter_index):
    """
    Submit Vote
    """
    # Perform deepcopy to prevent mutable value change
    voter = copy.deepcopy(voter_arr)
    # Translate vote to approprimate binary value for encryption, then back to decimal value m for encryption
    m = int("1".zfill(number_of_bits) + ''.join(["".zfill(number_of_bits) for i in range(0, vote - 1)]), 2)
    # perform paillier encryption
    r = random.randrange(1, n+1)
    C = int(((g**m)*(r**n)) % (n*n))
    # save encryption to file
    file = open("encrypted_vote.txt", "a")
    file.write(str(C) + " " + str(vote_id) + "\n")
    file.close()
    voter[voter_index][2] = "1"
    voter[voter_index][3] = str(vote_id)
    file_voter = open("voter.txt", "w")
    for i in voter:
        file_voter.write(' '.join(i) + "\n")
    file_voter.close()
    return voter

def has_all_vote(voter):
    for x in voter:
        if x[2] == "0":
            return 0
    return 1

def has_vote_end():
    file = open('vote_status.txt', 'r')
    if file.readline() == "1":
        return True
    return False


def execute_main():
    if not os.path.isfile('public.txt') or not os.path.isfile('voter.txt') or not os.path.isfile('vote_status.txt'):
        print("Some File are missing! Please re-run generation function in voting_authority.py file!")
        return
    if has_vote_end():
        print("Vote has ended! Please re-run generation function in voting_authority.py file to reset the election!")
        return
    n, g = get_public_key()
    voter = get_voter()
    run = True
    print("Simulate getting voter information (get voter name and id). In real use case, voter name and id (card_id) will be embeded in a smartcard. Voter will not be required to enter this information by hand.")
    while run:
        if has_vote_end():
            print("Vote has ended! Please re-run generation function in voting_authority.py file to reset the election!")
            break
        print("-----------------------------------------------------------")
        name = input("Enter your name (ex: Voter1): ")
        id = input(
            "Enter your card_id (card_id = the digit of your voter (ex: Voter1 -> card_id = 1 )): ")
        current_voter_index = get_voter_index(voter, name, id)
        if current_voter_index == -1:
            print("-----------------------------------------------------------")
            print("The infomration you provided is not correct! Your voter and id might not exists or it might not match our database! Please try again!")
            continue
        if has_voter_vote(voter, current_voter_index):
            print("-----------------------------------------------------------")
            print(name, "has voted! One voter can't submit 2 ballots!")
            continue
        vote = int(input(
            "Who do you want to vote for (1 to " + str(candidates) + "): "))
        while vote < 1 or vote > candidates:
            print("Incorrect vote! Please enter again!")
            vote = int(input(
                "Who do you want to vote for (1 to " + str(candidates) + "): "))
        vote_id = uuid4()
        voter = submit_vote(vote, vote_id, int(n), int(g),
                            voter, current_voter_index)
        print("-----------------------------------------------------------")
        print("Vote complete!")
        print("-----------------------------------------------------------")
        print("Your vote id is:", str(vote_id))
        print("You can use your vote id to see that your vote is on election bulletin board, assuring you that your vote has been submitted and will be counted in the election!")
        print("-----------------------------------------------------------")
        if has_all_vote(voter):
            vote_end.end()
            print("All voters has voted, vote has ended!")
            run = False
        else: 
            inp2 = input(
                "Continue voting as another person? Enter 1 for yes, other for no: ")
            if inp2 != "1":
                run = False
            else:
                voter = get_voter()


if __name__ == "__main__":
    execute_main()