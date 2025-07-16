def validate_announcement_payload(payload):
    urls = set()
    for material in payload.get("materials", []):
        url = (
            material.get("link", {}).get("url") or
            material.get("youtubeVideo", {}).get("alternateLink")
        )
        if url:
            if url in urls:
                raise ValueError(f"Enlace duplicado detectado: {url}")
            urls.add(url)
    return True