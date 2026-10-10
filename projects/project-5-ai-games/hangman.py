import random

WORDS = ["python", "finance", "startup", "agent", "vector", "flask"]


def masked(word: str, guesses: set[str]) -> str:
    return " ".join(letter if letter in guesses else "_" for letter in word)


def play():
    word = random.choice(WORDS)
    guesses = set()
    lives = 6
    lines = [
        "Bold guess.",
        "The keyboard is getting nervous.",
        "You might want a better strategy.",
        "Okay, that one actually helped.",
    ]

    while lives and any(letter not in guesses for letter in word):
        print(f"\n{masked(word, guesses)}   Lives: {lives}")
        guess = input("Guess a letter: ").lower().strip()[:1]
        if not guess.isalpha():
            continue
        if guess in guesses:
            print("Already guessed.")
            continue
        guesses.add(guess)
        if guess not in word:
            lives -= 1
            print(random.choice(lines))

    if lives:
        print(f"You got it: {word}")
    else:
        print(f"Game over. The word was {word}.")


if __name__ == "__main__":
    play()
