def normalize_counts(matches):
    result = {}

    for skill, aliases in matches.items():
        unique = set(aliases)

        # simple cap to avoid inflation
        count = min(len(unique), 3)

        result[skill] = count

    return result