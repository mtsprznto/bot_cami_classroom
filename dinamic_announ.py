



def create_announcement(
    text: str,
    add_link: bool = False,
    link_url: str = "",
    link_title: str = "",
    add_video: bool = False,
    video_id: str = "",
    video_title: str = "",
    add_form: bool = False,
    form_url: str = "",
    form_title: str = ""
) -> dict:
    materials = []

    if add_link:
        materials.append({
            "link": {
                "url": link_url,
                "title": link_title
            }
        })

    if add_video:
        materials.append({
            "youtubeVideo": {
                "id": video_id,
                "title": video_title,
                "alternateLink": f"https://www.youtube.com/watch?v={video_id}"
            }
        })

    if add_form:
        # No se puede usar el tipo 'form' directamente, así que va como link
        materials.append({
            "link": {
                "url": form_url,
                "title": form_title
            }
        })

    return {
        "text": text,
        "materials": materials
    }
   
   
