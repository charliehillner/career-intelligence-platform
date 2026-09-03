def build_observable_text(job: dict) -> str:
    parts = [
        job.get("title"),
        job.get("description"),
    ]

    return " ".join(
        part.strip()
        for part in parts
        if isinstance(part, str) and part.strip()
    )