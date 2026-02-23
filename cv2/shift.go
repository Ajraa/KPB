package main

var EnglishAlphabetRunes = []rune("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

func CaesarShift(input string, shift int) string {
	shiftedRunes := make([]rune, len(input))
	for i, r := range input {
		isFound := false
		for j, letter := range EnglishAlphabetRunes {
			if r == letter {
				shiftedIndex := (j + shift) % len(EnglishAlphabetRunes)
				shiftedRunes[i] = EnglishAlphabetRunes[shiftedIndex]
				isFound = true
				break
			}
		}
		if !isFound {
			shiftedRunes[i] = r
		}
	}
	return string(shiftedRunes)
}
