#include <stdint.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>

typedef enum {
	CASE_VIDE,
	CASE_ROBOT = 1,
	CASE_HUMAIN = 2
} Case;

typedef enum {
	ROBOT = 1,
	HUMAIN = 2
} Joueur;

const int LIGNES = 6;
const int COLONNES = 7;

typedef struct {
	Case cases[6][7];
} PythonPlateau;

typedef struct {
	uint64_t robot_mask;
	uint64_t player_mask;
} Plateau;

/// renvoie false si le placement n'est pas valide
static bool place(Plateau *plateau, Joueur player, int col) {
	uint64_t offset = (1 << col);
	if ((plateau->player_mask | plateau->robot_mask) & offset) return false;

	uint64_t limit = offset << 7*LIGNES;
	while (offset < limit) {
		if ((plateau->player_mask | plateau->robot_mask) & offset) break;

		offset <<= 7;
	}

	offset >>= 7;

	if (player == ROBOT) plateau->robot_mask |= offset;
	else plateau->player_mask |= offset;
	return true;
}

static inline uint8_t count_bits(uint64_t v) {
	return __builtin_popcountl(v);
}

// void print_bit_flag(uint64_t mask, char c) {
// 	uint8_t index = 0;
// 	uint64_t offset = 1;
// 	while (!(offset & ((uint64_t)1 << 42))) {
// 		if (mask & offset) printf("%c ", c);
// 		else printf("` ");
//
// 		index += 1;
// 		if (index % 7 == 0) printf("\n");
//
// 		offset <<= 1;
// 	}
// 	printf("\n");
// }

float evaluate(Plateau plateau) {
	uint64_t rs[2] = { plateau.player_mask, plateau.robot_mask };
	float score[2] = { 0.0, 0.0 };

	static const uint8_t shifts[4][3] = {
		{ 1, 2, 3 }, // horizontal
		{ 7, 14, 21 }, // vertical
		{ 8, 16, 24 }, // diagonal down
		{ 6, 12, 18 }  // diagonal up
	};

	static const uint64_t bands[4][3] = {
		{
			0b111111011111101111110111111011111101111110,
			0b111110011111001111100111110011111001111100,
			0b111100011110001111000111100011110001111000,
		},
		{
			0b111111111111111111111111111111111111111111,
			0b111111111111111111111111111111111111111111,
			0b111111111111111111111111111111111111111111,
		},
		{
			0b111111011111101111110111111011111101111110,
			0b111110011111001111100111110011111001111100,
			0b111100011110001111000111100011110001111000,
		},
		{
			0b011111101111110111111011111101111110111111,
			0b001111100111110011111001111100111110011111,
			0b000111100011110001111000111100011110001111
		}
	};

	for (int i = 0; i < 2; i++) {
		uint64_t r = rs[i];

		for (int idx = 0; idx < 4; idx++) {
			uint64_t mask = r & ((r & bands[idx][0]) >> shifts[idx][0]);
			score[i] += count_bits(mask);

			mask = mask & ((r & bands[idx][1]) >> shifts[idx][1]);
			score[i] += count_bits(mask) * 5.0;

			mask = mask & ((r & bands[idx][2]) >> shifts[idx][2]);
			if (mask) return INFINITY * (i*2 - 1);
		}
	}

	return score[1] - score[0];
}


float maxf(float a, float b) {
	return a > b ? a : b;
}

float minf(float a, float b) {
	return a < b ? a : b;
}

typedef struct {
	float score;
	// -1 pour un coup inconnu
	int coup;
	int profondeur;
} Minmax;

static Minmax internal_minmax(Plateau plateau, Joueur joueur, int profondeur, float alpha, float beta) {
	if (profondeur <= 0) {
		return (Minmax) {
			.score = evaluate(plateau),
			.coup = -1,
			.profondeur = profondeur
		};
	}

	float current_score = evaluate(plateau);
	// le joueur a gagné, il est inutile d'aller plus loin
	if (current_score == INFINITY || current_score == -INFINITY) {
		return (Minmax) {
			.score = current_score,
			.coup = -1,
			.profondeur = profondeur
		};
	}

	// on commence d'abords par les colonnes au centre, car elles possèdent de meilleur coups en moyenne
	// cela permet une plus grande optimisation de l'alpha-beta
	const static int ordre_colonnes[7] = {
		// 0, 1, 2, 3, 4, 5, 6
		3, 2, 4, 1, 5, 0, 6
	};

	if (joueur == ROBOT) {
		Minmax m = { .score = -INFINITY, .coup = -1, .profondeur = -1 };
		for (int col_idx = 0; col_idx < COLONNES; col_idx++) {
			int col = ordre_colonnes[col_idx];

			Plateau p = plateau;
			if (!place(&p, joueur, col)) continue;

			Minmax coup = internal_minmax(p, HUMAIN, profondeur - 1, alpha, beta);
			if (coup.score > m.score || (coup.score == m.score && (coup.score < 0 ^ coup.profondeur > m.profondeur)) || m.coup == -1) {
				m = coup;
				m.coup = col;
			}

			if (m.score > beta) break;
			alpha = maxf(alpha, m.score);
		}

		return m;
	} else {
		Minmax m = { .score = INFINITY, .coup = -1, .profondeur = -1 };
		for (int col_idx = 0; col_idx < COLONNES; col_idx++) {
			int col = ordre_colonnes[col_idx];

			Plateau p = plateau;
			if (!place(&p, joueur, col)) continue;

			Minmax coup = internal_minmax(p, ROBOT, profondeur - 1, alpha, beta);
			if (coup.score < m.score || (coup.score == m.score && (coup.score > 0 ^ coup.profondeur > m.profondeur)) || m.coup == -1) {
				m = coup;
				m.coup = col;
			}

			if (m.score < alpha) break;
			beta = minf(beta, m.score);
		}

		return m;
	}
}

Plateau array_to_bit_flag(Case cases[6][7]) {
	uint64_t player_mask = 0;
	uint64_t robot_mask = 0;

	uint64_t index = 1;

	for (int j = 0; j < LIGNES; j++) {
		for (int i = 0; i < COLONNES; i++) {
			switch (cases[j][i]) {
				case CASE_VIDE:
					break;
				case CASE_ROBOT:
					robot_mask |= index;
					break;
				case CASE_HUMAIN:
					player_mask |= index;
					break;
			}

			index <<= 1;
		}
	}

	return (Plateau) { robot_mask, player_mask };
}

Minmax minmax(PythonPlateau plateau, Joueur joueur, int profondeur) {
	Minmax m = internal_minmax(array_to_bit_flag(plateau.cases), joueur, profondeur, -INFINITY, INFINITY);
	return m;
}
