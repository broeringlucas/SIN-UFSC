word1 = input()
word2 = input()
if word1 == word2:
    print(False)
else:
    print(sorted(word1) == sorted(word2))