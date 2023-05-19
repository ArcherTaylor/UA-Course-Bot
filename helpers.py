def find_embed_color(course_prefix: str):
    import json

    with open('groups.json') as codes:
        data = json.load(codes)

    for college_name, college_data in data.items():
        if course_prefix in college_data['codes']:
            return college_data['color']
    return 0x00008B