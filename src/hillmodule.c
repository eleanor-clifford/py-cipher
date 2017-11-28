#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void frequencyAnalysis(char* ciphertext, int N, float ** out)
{
	float letterFrequency[] = {0.0817, 0.0149, 0.0278, 0.0425, 0.127, 0.0223, 0.0202, 0.0609, 0.0697, 0.0015, 0.0077, 0.0402, 0.0241, 0.0675, 0.0751, 0.0193, 0.0009, 0.0599, 0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 0.0197, 0.0007}; 
	int len = strlen(ciphertext);
	float expectedCounts[26];
	for (int i = 0; i < 26; i++) { expectedCounts[i] = letterFrequency[i] * len; }
	int permutation[N], letters[26], cipherSliceArray[N], letter;
	float chiSquared;
	float* results = malloc((int)pow(26,N) * sizeof(float)); 
	for (int p = 0; p < pow(26,N); p++) {
		for (int n = 0; n < N; n++) permutation[n] = (int)(p / pow(26,N-(n+1)))%26;
		for (int i = 0; i < 26; i++) letters[i] = 0;
		for (int l = 0; l < len / N; l++) {
			for (int i = 0; i < N; i++) { cipherSliceArray[i] = ciphertext[N*l + i] - 65; }
			letter = 0; for (int i = 0; i < N; i++) {
				letter += permutation[i] * cipherSliceArray[i];
			} letter = letter%26; letters[letter]++;
			chiSquared = 0; for (int i = 0; i < 26; i++) {
				chiSquared += pow(letters[i] - expectedCounts[i],2)/expectedCounts[i];
			}
		} results[p] = chiSquared;
	} *out = results;
}