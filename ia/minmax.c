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

typedef struct {
	Case cases[6][7];
} Plateau;

const int LIGNES = 6;
const int COLONNES = 7;

/// renvoie false si le placement n'est pas valide
static bool place(Plateau *plateau, Joueur player, int col) {
	if (plateau->cases[0][col] != CASE_VIDE) return false;

	int ligne_max = 0;
	while (ligne_max < LIGNES-1) {
		if (plateau->cases[ligne_max+1][col] != CASE_VIDE) break;
		ligne_max++;
	}

	plateau->cases[ligne_max][col] = (Case)player;
	return true;
}

static float evaluate(Plateau *plateau) {
	float score = 0.0;

	for (int j = 0; j < LIGNES; j++) {
		for (int i = 0; i < COLONNES; i++) {
			Case c = plateau->cases[j][i];
			if (c == CASE_VIDE) continue;

			float multiplier = c == CASE_ROBOT ? 1.0 : -1.0;

			int dirs[][2] = {
				{ 1, 0 },
				{ 0, 1 },
				{ 1, 1 },
				{ 1,-1 },
			};

			for (int dir = 0; dir < 4; dir++) {
				int idx = 1;
				while (idx < 4) {
					int dx = i + dirs[dir][0]*idx;
					int dy = j + dirs[dir][1]*idx;

					if (dx < 0 || dx >= COLONNES || dy <= 0 || dy >= LIGNES) break;

					Case autre = plateau->cases[dy][dx];
					if (c != autre) break;

					idx++;
				}

				if (idx == 2) score += 1.0 * multiplier;
				else if (idx == 3) score += 5.0 * multiplier;
				else if (idx == 4) return INFINITY * multiplier;
			}
		}
	}

	return score;
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

static Minmax internal_minmax(Plateau *plateau, Joueur joueur, int profondeur, float alpha, float beta) {
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

			Plateau p = *plateau;
			if (!place(&p, joueur, col)) continue;

			Minmax coup = internal_minmax(&p, HUMAIN, profondeur - 1, alpha, beta);
			if (coup.score > m.score || (coup.score == m.score && coup.profondeur > m.profondeur)) {
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

			Plateau p = *plateau;
			if (!place(&p, joueur, col)) continue;

			Minmax coup = internal_minmax(&p, ROBOT, profondeur - 1, alpha, beta);
			if (coup.score < m.score || (coup.score == m.score && coup.profondeur > m.profondeur)) {
				m = coup;
				m.coup = col;
			}

			if (m.score <= alpha) break;
			beta = minf(beta, m.score);
		}

		return m;
	}
}

Minmax minmax(Plateau plateau, Joueur joueur, int profondeur) {
	return internal_minmax(&plateau, joueur, profondeur, -INFINITY, INFINITY);
}
