

import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
import random
import tkinter as tk
from functools import partial
import pyperclip  # For clipboard functionality

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

stop_words = stopwords.words("english")

def plagiarism_remover(word):
    """Function to find a synonym for the word, avoiding stop words."""
    synonyms = []
    
    # Return word directly if it's a stopword or has no synonyms
    if word in stop_words or not wordnet.synsets(word):
        return word

    # Collect all synonyms
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    pos_tag_word = nltk.pos_tag([word])[0][1]  # Get POS tag of the word
    final_synonyms = [syn for syn in synonyms if nltk.pos_tag([syn])[0][1] == pos_tag_word]
    final_synonyms = list(set(final_synonyms))  # Remove duplicates
    
    if not final_synonyms:
        return word
    
    # Return synonym with correct case formatting
    return random.choice(final_synonyms).title() if word.istitle() else random.choice(final_synonyms)

def plagiarism_removal(para):
    """Function to remove plagiarism from the given paragraph."""
    para_split = word_tokenize(para)
    final_text = [plagiarism_remover(word) for word in para_split]
    return " ".join(final_text)

# Function to copy text to clipboard
def copy_to_clipboard(text):
    """Copies the given text to the clipboard."""
    pyperclip.copy(text)

# GUI Functions
def call_result(label_result, entry, copy_btn):
    """Function to display the result in the GUI and enable copy button."""
    text = entry.get()
    result = plagiarism_removal(text)
    label_result.config(text="Text after plagiarism removal is:\n %s" % result, wraplength=500)
    
    # Enable the "Copy to Clipboard" button and store the result
    copy_btn.config(state="normal")
    copy_btn.result_text = result

def copy_action(copy_btn):
    """Handles the action to copy text to clipboard when button is clicked."""
    result_text = copy_btn.result_text
    copy_to_clipboard(result_text)

# Set up GUI
root = tk.Tk()
root.geometry('600x400')  # Adjusted the window size for better UX
root.title('Plagiarism Removal')

# Input Text Label and Entry Box
labelNum1 = tk.Label(root, text="Enter text to remove plagiarism:")
labelNum1.grid(row=1, column=0, padx=10, pady=10)
entryNum1 = tk.Entry(root, textvariable=tk.StringVar(), width=60)
entryNum1.grid(row=1, column=1, padx=10, pady=10)

# Result Label
labelResult = tk.Label(root, text="")
labelResult.grid(row=3, column=1, padx=10, pady=10)

# Button to call plagiarism removal
call_result_btn = partial(call_result, labelResult, entryNum1)
buttonCal = tk.Button(root, text="Remove Plagiarism", command=lambda: call_result(labelResult, entryNum1, copy_btn))
buttonCal.grid(row=2, column=1, pady=20)

# Button to copy result text to clipboard
copy_btn = tk.Button(root, text="Copy to Clipboard", command=lambda: copy_action(copy_btn), state="disabled")
copy_btn.grid(row=4, column=1, pady=10)

root.mainloop()
