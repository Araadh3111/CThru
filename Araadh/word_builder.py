recognized_letters = []

while True:
    letter = input("Enter Recognized letter:  ")

    if letter == "space":
        recognized_letters.append(" ")

    else:
        recognized_letters.append(letter)

    word = "".join(recognized_letters)

    print("Current text:", word)