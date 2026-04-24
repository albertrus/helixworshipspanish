def build_filename(track_number: int, artist_style: str, tone_type: str) -> str:
    """
    Build a preset filename following the convention:
    {track_number:02d}_{artist_style}_{tone_type}.hlx

    artist_style and tone_type are auto-translated if an English key is found.
    """
    tone_es = WORSHIP_TRANSLATIONS.get(tone_type, tone_type)
    return f"{track_number:02d}_{artist_style}_{tone_es}.hlx"


WORSHIP_TRANSLATIONS = {
    # Styles
    "Clean": "Limpio",
    "Drive": "Drive",
    "Crunch": "Crujiente",
    "Lead": "Solo",
    "Heavy": "Pesado",

    # Effects
    "Ambient": "Ambiente",
    "Swell": "Etéreo",
    "Delay": "Delay",
    "Reverb": "Reverb",
    "Chorus": "Chorus",
    "Modulation": "Modulación",

    # Tones
    "Bright": "Brillante",
    "Warm": "Cálido",
    "Dark": "Oscuro",
    "Punchy": "Potente",
    "Smooth": "Suave",

    # Common phrases
    "Worship": "Adoración",
    "Essentials": "Esenciales",
    "Latin": "Latino",
    "Modern": "Moderno",
    "Classic": "Clásico",
}
