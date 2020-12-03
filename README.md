## Paillier Homomorphic E-voting system

Python implementation of an e-voting system using Paillier homomorphic encryption.

---
**RMIT University Vietnam**

**COSC2539 - Security in Computing and Information Systems** 

**s3804737 - Dinh Long Nguyen**

**Semester 3 - 2020**

Note: 
- This is a submission for **`COSC2539 Assignment 1 - Section 2 - Topic B.2`**. This project is my original work. All of the information and idea which was not originally mine has been properly cited and referenced. This repository was set to public to assist the marking process for lecturer. I strictly adhere to RMIT Academic Integrity guidelines and I have no intention of plagiarising or allowing anyone to plagiarise.
- This project has been finalized before the assignment deadline. 

---
### How does this project works? How was this project structured?

This project is designed based on RMIT COSC2539 Lecture 5: "Preserving Privary" homormophic e-voting examples (Crellin, "Lecture 5: Prserving Privacy", n.d., Crellin, "relp.it: Paillier Encryption Example", n.d.). The addition of bulletin board and `vote_id` was inspired by a research from MIT and a informative video from professor Ron Rivest (Berke, 2020; Rivest, 2016).

This project has a total of 6 python files, each have its own dedicated functionalities:
1. `config.py`: config variables for the project (very crucial for setting up the project).
2. `voting_authority.py`: Voting authority (election board) program, which is used to generate Paillier public & secret key and other data such as voter information (stored in `voter.txt`) and other config information, as well to decrypt the final homomorphic data coming from the server.
3. `vote.py`: program used for voting in voting booth. This program asllow user to enter their user information and cast their vote. The information that voter enter will be checked with the database to verify that the voter has valid name and id (card_id) (voter data stored in `voter.txt`). The voter's vote will then be encrypted using Paillier public key generated above. The encrypted data will be saved in a text file. The console will then return the state of the vote as successful and return a `vote_id`, which can be used to check for the vote availability on bulletin board (`bulletin_board.py`). Each voter will only be allowed to vote once. When all voters has voted, the voting process will end automatically.
4. `vote_end.py`: execution of this program will immdediately end the voting process (allow the vote to end early without the vote of all voters in database).
5. `bulletin_board.py`: this program requires `vote_id` as input. The program will then procceed to check if `vote_id` match with any available vote, allowing voter to verify that their vote is in the vote poll and it will be counted towards the final result.
6. `homomorphic_server.py`: a program to combine all the votes from the voting process and encrypted them homomorphically. This program will return an encrypted data from all the votes and can only used when the voting process has ended.

The neccessary data for the election will be firstly generated by `voting_authority.py`. Other information such as encrypted data will be generated later on by `voter.py`, `homomorphic_server.py`, and `vote_end.py`. There are a total of 6 txt files:
1. `public.txt`: store public key for Paillier encryption (n, g)
2. `private.txt`: store private key for Paillier decryption (n, Lambda, Meu)
3. `voter.txt`: store voter information (name, id[card_id], has_voter_voted, vote_id)
4. `encrypted_vote.txt`: store encrypted vote data (vote_data, vote_id)
5. `vote_status.txt`: contain a single binary value (0,1) indicating if the voting process has ended (0 = not ended, 1 = ended)
6. `homomorphic_vote.txt`: contain the data produced by homomorphic encryption from homomorphic_server.py

![Project Structure](https://user-images.githubusercontent.com/45910030/100973065-76c08280-356c-11eb-89bb-3cdafb8014e5.png)

Image 1: Diagram on how this project works and was structured (Crellin, "Lecture 5: Prserving Privacy", n.d.; Crellin, "relp.it: Paillier Encryption Example", n.d.; Berke, 2020, Rivest, 2016)

---
### How to run

**Requirements:** `Python 3.x` (project tested on `Python 3.7.1` and `Python 3.8.3`)

**Step 0: Configuration**

Change configuration in `config.py` if you need to.

Navigate to the source code folder before carrying on to the next step

**Step 1: Paillier key genaration, data generation**

  ```bash
  #run voting_authority.py
  python voting_authority.py
  ```
  After execution, the file will ask you to choose which options (1, 2). For data genaration, enter `1`.
  
  The program will then ask you to choose whether you want to test out the encryption key with your message or not. If yes, enter `1`.
  
  You will then see the details of all the process that has happened.
  
  If no config variable has changed there will be 3 voter generated. Each voter will have a name and an id. Voter index will start from 1. The default voter names and ids are (`Voter1` , `1`), (`Voter2` , `2`), (`Voter3` , `3`).
  
  Check if 4 txt files: `voter.txt`, `public.txt`, `private.txt`, and `vote_status.txt` has been generated. Move on if the requirement is satisfied.
 
**Step 2: Voting Process**

  ```bash
  #start voting
  python vote.py
  ```
  
  Enter voter name and id. The program will perform various check on voter name and id.
  
  Carry on to casting the vote *(Default: 1-4)*.
  
  After casting the vote, the program will return a `vote_id`, which can be used to track the vote in bulletin board.
  
  The vote encrypted data will be saved to `encrypted_vote.txt`.
  
  The program will the ask if the user want to vote again with another voter. If all voters have voted, the voting process will end and the program will automatically closed.
  
  ```bash
  #start bulletin board
  python bulletin_board.py
  ```
  
  Enter the `vote_id` from above to check if your vote is available on the election bulletin board
  
  ```bash
  #end voting process
  python vote_end.py
  ```
  
  End voting process early, not requiring the votes of all voters.
  
**Step 3: Homomorphic encryption**

  ```bash
  #start server code
  python homomorphic_server.py
  ```
  
  The program can only be executed when the voting process has ended. 
  
  Perform homomorphic encryption on all encrypted vote data. Return a value to file `homomorphic_vote.txt`
  
 **Step 4: Decrption and view election result**
  
  ```bash
  #run voting_authority.py
  python voting_authority.py
  ```
  
  After execution, the file will ask you to choose which options (1, 2). For data decryption and result, enter `2`.
  
  The program will then perform decryption on data from `homomorphic_vote.txt` and print out the final election results.
  
---

### Config Variable Explanation

Project config (environment) variables are stored in `config.py`:
- **prime_upperbound** *(Default = 100)*, **prime_lowerbound** *(Default = 0)*: upper and lower bound for `p` and `q` prime number random generations. It is important to remember that `n = p * q`, so changing prime_upperbound and prime_lowerbound might require you to change `minimum_n_value`.
- **number_of_candidates* *(Default = 4)*: the total number of candidates in the election. 
- **number_of_bits** *(Default = 2)*: the total number of binary bits that will represent the number of vote for each candidate (if number_of_bits = 2 --> the largest number of voter is `11 (binary)` or `3 (decimal)`). Because of that, this variable directly affects the total number of voters.
- **voter** *(Default = 3)*": the total number of voter for this election. This variable is directly affected by `number_of_bits` variable.
- **minimum_n_value** *(Default = 256, calculated automatically by the program)*: the minimum number for `n` in Paillier encryption key. This variable is directly influenced by `number_of_candidates` and `number_of_bits` variables as both of these variables are the key to deciding how many total bits to use (ex: default is 4 candidates and 2 bits --> total number of bits for message m = 8 binary bits --> because the final decryption key is x mod `n`, to produce the final result as an 8 bit binary, n must be at least larger than 8 bits hence > 256 decimal).

---
### What is homomorphic encryption?

Homomorphic encryption is an encryption technique which "allows for computations on ciphertexts so that the decrypted result of the computations is the same as if the computations had been on the unencrypted values" (Berke, 2020).

---
### Why use homomorphic encryption for e-voting? 

As the voting process needs to be submitted anonymously and the result of each vote must remain encrypted throughout all the process (from voting booth, to voting server, to voting authority (election board)), homomorphic encryption allows encrypted data from the voting booth to be combined and encrypted in the voting server without having to do any decryption while still producing the same final result as being combined at the first stage before any encryption occurs (Berke, 2020, Saproo, Warke, Pote & Dhumal, 2020).

---
### How Paillier homomorphic encryption works on this e-voting implementation? 

After getting the message from voter, the data will be encrypted for each voter. All of the encrypted data from all voters will then be combined homomorphically, producing a single encrypted data. The single encrypted data will then be decrypted, which will output a result similar to the data which combined all the votes before any encryptions occur.

**Step 1: Get the message**

In default config value, there are a total of 2 binary bits --> maximum 3 (decimal) vote for each candidate vote count. If there are 4 candidates, each vote cast should be 2 (bits) * 4 (candidates) = 8 binary bits, with each 2 bits dedicated to each candidates. In this case, the voting message should be like this for all 4 candidates: 
- For candidate 1 (first candidate), the binary vote should be: 00 00 00 01 --> message in decimal `m = 1`
- For candidate 2 (second candidate), the binary vote should be: 00 00 01 00 --> message in decimal `m = 4`
- For candidate 3 (third candidate), the binary vote should be: 00 01 00 00 --> message in decimal `m = 16`
- For candidate 4 (fourth candidate), the binary vote should be: 01 00 00 00 --> message in decimal `m = 64`

If the binary bits is increased to 3 and the number of candidates remains 4, each 3 bits will be dedicated to each voter and the voting message should be represented accordingly: 
- For candidate 1 (first candidate), the binary vote should be: 000 000 000 001 --> message in decimal `m = 1`
- For candidate 2 (second candidate), the binary vote should be: 000 000 001 000 --> message in decimal `m = 8`
- ... The same for candidate 3, 4

**Step 2: Encrypt the message**

After successfully generating the message m, m will be encrypted using Paillier encryption. The encrypted data will be saved in a designated location.

**Step 3: Homomorphically encrypt all the messages**

After the voting process is done at the voting location, all the votes will be sent to a server which will then perform homomorphic encryption on all of the data. The encryption will produce a single encrypted result, which be then be saved in a designated location.

**Step 4: Decrypt the Homomorphically encrypted message**

Decrypt the data coming from the server. This decrypted data, which has been homomorphically encrypted, should return the same value as the decrypted data which have been combined (voting_process) before being encrypted.

---
### Project detail

The Paillier encryption key, from selecting prime `p` and `q` values and `g` value, to calculation for other values, are genearted automatically in `voting_authority.py`. Selecting the `r` value for encryption in `vote.py` is also done automatically. To properly genearte the key, I have looked into how other researchers has implemented the checking rules for auto generated key (Nassar, Erradi & Malluhi, 2015; Clark, 2020). Some of the rules that were implemented include:
- gcd(p*q, (p-1)*(q-1)) = 1
- g are in range from 1 to n^2
- insuring modular inverse calculation has a valid result
- random r in range from 1 to n


The voter data is also generated automatically in `voting_authority.py`. Each voter has a format of (name, id, has_voter_voted, vote_id). The voter id in this case is an id for an external system (ex: a smartcard id). In real life [example from 2012 US election e-voting machine](https://www.youtube.com/watch?v=aFrpgJLqW7c), this card might be given (dedicated) to users before they enter the vote and when voting, the voting machine can read the information from the card to verify who is voting ("This is how you vote in the United States!", 2012). In this program `vote.txt`, the voter has to enter their name and their id manually. The system will check if the user info entered is correct or not. 

This e-voting project is created based on a few of these rules and assumptions: 
- Each voter can only vote once
- Voting process can end early (some people might not show up to the election process)
- Each voter are given a vote_id, which can be used to verify if the vote has been appropriately submitted by search the vote_id on the election bulletin board `bulletin_board.py`.
- Using the vote_id, the voter can't verify who they have voted for through the bulletin board. The above statement ensure that the voter cannot sell their vote. For those who need to verify the vote (for assurance that the system is working properly), the system can still use the original private key to decode the message. If this case happens, the vote should be discarded [Not yet implemented].

The code replicates the use of 3 different sets of computers in the election: voting authority (election board) computer, voting booth computer, and powerful servers which is used for homomorphic encryption: 
- Voting authority computer is responsible for generating the Paillier public and private key, as well as decrypting the data coming from the server after the data from the voting booths have been encrypted homomorphically.
- Server is responsible for performing hard mathematical equations which requires expensive multiplication and modulus computations.
- Voting booth computers are responsible for getting the voter vote, encrypting the vote, and store the vote anonymously in an appropriate place. It is also important to make sure that each voter can only vote once. In this program, the voter detail `voter.txt` stored information on whether a person has voted. The encrypted data of the vote is stored seperately `encrypted_vote.txt` from the voter detail.

As a simple project which is created as a proof of concept (PoC), this project doesn't use any external library, utilizing only python built-in libraries. The encryption and decryption functions even though doesn't depend on any external library, the code for Paillier encryption and decryption are based on RMIT COSC2539 example code for Paillier encryption, which can be found [here](https://repl.it/@joncrel/PallierEcryption#main.py) (Crellin, "relp.it: Paillier Encryption Example", n.d.).

The use of file for storing information is just a temporary solution. In real use case, this data shouldn't be stored on a text file and should be stored in secured databases. Some data might only be available on one computer and not the others. To transfer data between computers (processes), there should be secured online connections between computers.

---
### References

Berke, A. (2020). Crypto Voting + US Elections: Reality – MIT Media Lab. Retrieved 2 December 2020, from https://www.media.mit.edu/posts/crypto-voting-us-elections-reality/

Clark, W. (2020). What is the Paillier cryptosystem?. Retrieved 2 December 2020, from https://blog.openmined.org/the-paillier-cryptosystem/

Crellin, J. (2020). Paillier Encryption Example. Retrieved 3 December 2020, from https://repl.it/@joncrel/PallierEcryption#main.py

Crellin, J. Security in Computing and Information Technology Lecture 4: Public Key Cryptography II. Lecture.

Crellin, J. Security in Computing and Information Technology Lecture 5: Preserving Privacy. Lecture.

Nassar, M., Erradi, A., & Malluhi, Q. (2015). Paillier's encryption: Implementation and cloud applications. doi: 10.1109/ARCSE.2015.7338149

Rivest, R. (2016). Was YOUR vote counted? (feat. homomorphic encryption). Retrieved 2 December 2020, from https://www.youtube.com/watch?v=BYRTvoZ3Rho. Video.

Saproo, S., Warke, V., Pote, S., & Dhumal, R. (2020). Online Voting System using Homomorphic Encryption. Retrieved 2 December 2020, from https://www.itm-conferences.org/articles/itmconf/pdf/2020/02/itmconf_icacc2020_03023.pdf

This is how you vote in the United States!. (2012). Retrieved 2 December 2020, from https://www.youtube.com/watch?v=aFrpgJLqW7c. Video.
