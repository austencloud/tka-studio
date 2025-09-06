import { Letter } from './Letter';

const letterFilenameMap: Record<string, Letter[]> = {
	Omega: [Letter.Ω, Letter.Ω_DASH],
	Theta: [Letter.θ, Letter.θ_DASH],
	Sigma: [Letter.Σ, Letter.Σ_DASH],
	Delta: [Letter.Δ, Letter.Δ_DASH],
	Phi: [Letter.Φ, Letter.Φ_DASH],
	Psi: [Letter.Ψ, Letter.Ψ_DASH],
	Lambda: [Letter.Λ, Letter.Λ_DASH],
	Alpha: [Letter.α],
	Beta: [Letter.β],
	Gamma: [Letter.Γ],
	W: [Letter.W_DASH],
	X: [Letter.X_DASH],
	Y: [Letter.Y_DASH],
	Z: [Letter.Z_DASH]
} as const;

const letterToFilenameMap: Partial<Record<Letter, string>> = Object.entries(
	letterFilenameMap
).reduce(
	(acc, [filename, letters]) => {
		letters.forEach((letter) => (acc[letter] = filename));
		return acc;
	},
	{} as Partial<Record<Letter, string>>
);

export function safeAsciiName(letter: Letter): string {
	return letterToFilenameMap[letter] ?? letter.toString();
}
