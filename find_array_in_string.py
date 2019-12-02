possible_matches = ['a', 'P', 'e', 'i', 'o', 'u', 'hell']
string = "hello people"

first_match = next((i for i in possible_matches if i.lower() in string.lower()), False)
print('first match, case insensitive: {}'.format(first_match))

all_matches = [i for i in possible_matches if i in string]
print('all matches: {}'.format(all_matches))

all_matches_deduped = {i for i in possible_matches if i in string}
print('all matches, deduped: {}'.format(all_matches_deduped))

all_matches_deduped_ordered = []
for i in possible_matches:
    if i in string and i not in all_matches_deduped_ordered:
        all_matches_deduped_ordered.append(i)
print('all matches, deduped and in order: {}'.format(all_matches_deduped_ordered))