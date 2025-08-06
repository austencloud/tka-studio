from __future__ import annotations


class LetterType:
    TYPE1 = "Type1"
    TYPE2 = "Type2"
    TYPE3 = "Type3"
    TYPE4 = "Type4"
    TYPE5 = "Type5"
    TYPE6 = "Type6"

    ALL_TYPES = [TYPE1, TYPE2, TYPE3, TYPE4, TYPE5, TYPE6]

    @classmethod
    def get_letter_type(cls, letter: str) -> str:
        type1_letters = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
        ]
        type2_letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
        type3_letters = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"]
        type4_letters = ["Φ", "Ψ", "Λ"]
        type5_letters = ["Φ-", "Ψ-", "Λ-"]
        type6_letters = ["α", "β", "Γ"]

        if letter in type1_letters:
            return cls.TYPE1
        if letter in type2_letters:
            return cls.TYPE2
        if letter in type3_letters:
            return cls.TYPE3
        if letter in type4_letters:
            return cls.TYPE4
        if letter in type5_letters:
            return cls.TYPE5
        if letter in type6_letters:
            return cls.TYPE6
        return cls.TYPE1

    @classmethod
    def get_type_description(cls, letter_type: str) -> tuple[str, str]:
        """Get the correct Legacy section names and descriptions."""
        descriptions = {
            cls.TYPE1: ("Dual-Shift", "Type1"),
            cls.TYPE2: ("Shift", "Type2"),
            cls.TYPE3: ("Cross-Shift", "Type3"),
            cls.TYPE4: ("Dash", "Type4"),
            cls.TYPE5: ("Dual-Dash", "Type5"),
            cls.TYPE6: ("Static", "Type6"),
        }
        return descriptions.get(letter_type, ("Unknown", "Type ?"))
