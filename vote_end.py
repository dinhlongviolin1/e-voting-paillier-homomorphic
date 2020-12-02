def end():
    file = open("vote_status.txt", "w")
    file.write("1")
    file.close()

if __name__ == "__main__":
    end()