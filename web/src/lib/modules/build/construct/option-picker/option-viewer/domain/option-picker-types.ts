

// ===== Basic State Types =====
export type OptionPickerState = 'loading' | 'ready' | 'error';

// ===== Sort and Filter Types =====
export type SortMethod = 'type' | 'endPosition' | 'reversals';

// ===== Type Filter Types =====
export type TypeFilter = {
  type1: boolean; // Dual-Shift (A-V)
  type2: boolean; // Shift (W, X, Y, Z, Σ, Δ, θ, Ω)
  type3: boolean; // Cross-Shift (W-, X-, Y-, Z-, Σ-, Δ-, θ-, Ω-)
  type4: boolean; // Dash (Φ, Ψ, Λ)
  type5: boolean; // Dual-Dash (Φ-, Ψ-, Λ-)
  type6: boolean; // Static (α, β, Γ)
};

