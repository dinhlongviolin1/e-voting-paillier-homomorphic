# RMIT University Vietnam
# Dinh Long Nguyen - s3804737
# vote.py

import os.path
import os
import random
import copy
import vote_end
from uuid import uuid4

# import neccesary config
from config import number_of_bits, number_of_candidates

# defining functions
def get_public_key():
    """
    get public key from file
    """
    file = open("public.txt", "r")
    data = file.readline().split(" ")
    n = data[0]
    g = data[1]
    print("Get public key completed!")
    return (n, g)


def get_voter():
    """
    get voter list from file
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
    get index of current voter based on name and id if available
    """
    # return -1 if no voter info found
    ans = -1
    for i in range(0, len(voter)):
        # criteria to find voter
        if voter[i][0] == name and voter[i][1] == id:
            ans = i
    return ans


def has_voter_vote(voter, index):
    """
    check to see if voter has voted
    """
    return voter[index][2] != "0"


def submit_vote(vote, vote_id, n, g, voter_arr, voter_index):
    """
    Submit Vote
    1. generate message m based on the total number of bits
    2. encrypt message m 
    3. output encrypted vote detail to file
    4. Update voter detail
    4. return updated voter list
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
    # Update voter info
    voter[voter_index][2] = "1"
    voter[voter_index][3] = str(vote_id)
    # write updated detail to file
    file_voter = open("voter.txt", "w")
    for i in voter:
        file_voter.write(' '.join(i) + "\n")
    file_voter.close()
    # return updated voter
    return voter

def has_all_vote(voter):
    """
    Check to see if all voters has voted to determine whether the vote can end
    """
    for x in voter:
        if x[2] == "0":
            return 0
    return 1

def has_vote_end():
    """
    Check to see if the vote has been ended
    """
    file = open('vote_status.txt', 'r')
    if file.readline() == "1":
        return True
    return False


def execute_main():
    # Check to see if necessary files is available
    if not os.path.isfile('public.txt') or not os.path.isfile('voter.txt') or not os.path.isfile('vote_status.txt'):
        print("Some File are missing! Please re-run generation function in voting_authority.py file!")
        return
    # Check to see if election has ended
    if has_vote_end():
        print("Vote has ended! Please re-run generation function in voting_authority.py file to reset the election!")
        return
    # Initialize data
    n, g = get_public_key()
    voter = get_voter()
    run = True
    print("Simulate getting voter information (get voter name and id). In real use case, voter name and id (card_id) will be embeded in a smartcard. Voter will not be required to enter this information by hand.")
    while run:
        # Check to see if vote has ended after each loop
        if has_vote_end():
            print("Vote has ended! Please re-run generation function in voting_authority.py file to reset the election!")
            break
        # Enter voter info
        print("-----------------------------------------------------------")
        name = input("Enter your name (ex: Voter1): ")
        id = input(
            "Enter your card_id (card_id = the digit of your voter (ex: Voter1 -> card_id = 1 )): ")
        # get voter index in list
        current_voter_index = get_voter_index(voter, name, id)
        # if voter is not found
        if current_voter_index == -1:
            print("-----------------------------------------------------------")
            print("The infomration you provided is not correct! Your voter and id might not exists or it might not match our database! Please try again!")
            continue
        # check to see if voter has voted
        if has_voter_vote(voter, current_voter_index):
            print("-----------------------------------------------------------")
            print(name, "has voted! One voter can't submit 2 ballots!")
            continue
        # enter vote option
        vote = int(input(
            "Who do you want to vote for (1 to " + str(number_of_candidates) + "): "))
        # Validate vote input
        while vote < 1 or vote > number_of_candidates:
            print("Incorrect vote! Please enter again!")
            vote = int(input(
                "Who do you want to vote for (1 to " + str(number_of_candidates) + "): "))
        # Genterate vote_id using uuid library
        vote_id = uuid4()
        # Submit vote
        voter = submit_vote(vote, vote_id, int(n), int(g),
                            voter, current_voter_index)
        print("-----------------------------------------------------------")
        print("Vote complete!")
        print("-----------------------------------------------------------")
        print("Your vote id is:", str(vote_id))
        print("You can use your vote id to see that your vote is on election bulletin board, assuring you that your vote has been submitted and will be counted in the election!")
        print("-----------------------------------------------------------")
        # Check to see if all voter has voted
        if has_all_vote(voter):
            # End vote process if all voter has voted
            vote_end.end()
            print("All voters has voted, vote has ended!")
            run = False
        else: 
            # Allow user to decide to continue voting or not
            inp2 = input(
                "Continue voting as another person? Enter 1 for yes, other for no: ")
            if inp2 != "1":
                run = False
            else:
                # reset voter list data if user continue to vote
                voter = get_voter()

# Main function
# Run if the file is executed directly (not through import)
if __name__ == "__main__":
    execute_main()