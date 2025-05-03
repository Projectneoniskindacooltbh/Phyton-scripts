import random

# List of 5-letter words (you can expand this)
word_list = ["apple", "brick", "crane", "flint", "glove", "house", "joker", "liver", "pride", "shiny", "track", "chick"]

# Pick a random word
secret_word = random.choice(word_list)

def get_feedback(guess, secret):
    feedback = ""
    for i in range(5):
        if guess[i] == secret[i]:
            feedback += guess[i].upper()  # Correct letter and position
        elif guess[i] in secret:
            feedback += guess[i].lower()  # Correct letter, wrong position
        else:
            feedback += "_"              # Wrong letter
    return feedback

print("Welcome to Wordle (Python edition)!")
print("Guess the 5-letter word. You have 6 tries.\n")

attempts = 6

while attempts > 0:
    guess = input("Enter your guess: ").lower()
    if len(guess) != 5:
        print("Please enter a 5-letter word.")
        continue
    if guess not in word_list:
        print("Word not in list. Try again.")
        continue

    feedback = get_feedback(guess, secret_word)
    print("Feedback:", feedback)

    if guess == secret_word:
        print("🎉 Congratulations! You guessed the word!")
        break

    attempts -= 1
    print(f"Tries left: {attempts}")

if attempts == 0 and guess != secret_word:
    print(f"Game over! The word was: {secret_word}")
