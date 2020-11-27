import random

def generate_password():
    result = ""

    letters = "qwertyuiopasdfghjklzxcvbnm"
    letters = list(letters)

    while(len(result) != 16):
        
        letter = random.choice(letters)

        if (random.randint(0, 1) == 1):
            letter = letter.upper()
            result += letter + str(random.randint(0, 9))
        else:
            result += letter + str(random.randint(0, 9))

    return result

password = generate_password()

print(password)