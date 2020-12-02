# RMIT University Vietnam
# Dinh Long Nguyen - s3804737
# vote_end.py

def end():
    # Change vote status data to "1", which indicates that the voting process has ended
    file = open("vote_status.txt", "w")
    file.write("1")
    file.close()
    print("Voting process has been ended!")

# Main function
# Run if the file is executed directly (not through import)
if __name__ == "__main__":
    end()