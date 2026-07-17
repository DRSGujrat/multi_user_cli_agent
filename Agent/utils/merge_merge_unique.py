def merge_unique(old_list, new_list):
    
    seen = set(old_list)

    for item in new_list:
        item = item.lower()

        if item not in seen:
            old_list.append(item)
            seen.add(item)

    return old_list
def merge(s1, extracted_profile):

    profile = s1

    profile.goals = merge_unique(
        profile.goals,
        extracted_profile.goals
    )

    profile.preferences = merge_unique(
        profile.preferences,
        extracted_profile.preferences
    )

    profile.hobbies = merge_unique(
        profile.hobbies,
        extracted_profile.hobbies
    )

    profile.likes = merge_unique(
        profile.likes,
        extracted_profile.likes
    )

    profile.dislikes = merge_unique(
        profile.dislikes,
        extracted_profile.dislikes
    )

    profile.projects = merge_unique(
        profile.projects,
        extracted_profile.projects
    )

    profile.skills = merge_unique(
        profile.skills,
        extracted_profile.skills
    )
