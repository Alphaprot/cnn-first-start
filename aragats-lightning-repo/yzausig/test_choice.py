question = "Do you want to:\n"
option1 = "[1] Create training data from the converted images\n"
option2 = "[2] Train neural network by providing existing training data as .npy\n"
option3 = "[3] Display images\n"
options = [question, option1, option2, option3]

prompt = [" [Enter digit] "]
validInput =    {"1":1,
                "2":2,
                "3":3}


print(*options + prompt)
choice = input().lower()
print(choice)
