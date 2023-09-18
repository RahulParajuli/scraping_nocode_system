import re

# New etraction function with regex 

def extract(text):
    name_regex = r'^([^\n]+)'
    # number_finder = r'\+\d{1,3}(?:[-\s]?\d{1,4}){1,5}'
    number_finder=r'(?<!\d)(?:\d[\d\s-]*){5,}(?!\d)'
    location_pattern = r'\b\w+\n\w+(?:,\s\w+)+\s\w+\b'

    # Extract name
    name_holder = re.search(name_regex, text)
    name = name_holder.group() if name_holder else None

    # Extract number
    number_holder = re.search(number_finder, text)
    number = number_holder.group() if number_holder else None

    # Extract location
    location_holder = re.search(location_pattern, text)
    location = location_holder.group() if location_holder else None

    details = {
        'Company name': name,
        'Company number': number,
        'Company location': location
    }
    return details













#uncomment to get list dictionaries for the details

# def extractor(document):
#     if not isinstance(document, list):
#         print("Input must be a list.")
#         return

#     name_regex = r'^([^\n]+)'
#     number_finder = r'\+\d{1,3}(?:[-\s]?\d{1,4}){1,5}'
    
#     extracted_data = []

#     for text in document:
#         number_holder = re.search(number_finder, text)
#         number = number_holder.group() if number_holder else None

#         name_holder = re.search(name_regex, text)
#         name = name_holder.group() if name_holder else None

#         start_index = text.find('\n+')

#         if start_index != -1:
#             # Find the index of the nearest preceding '\n'
#             preceding_newline_index = text.rfind('\n', 0, start_index)

#             # Extract the text between '\n' and '\n+'
#             if preceding_newline_index != -1:
#                 location = text[preceding_newline_index + 1 : start_index]
#             else:
#                 location = None
#         else:
#             location = None

#         details = {
#             'Company name': name,
#             'Company number': number,
#             'Company location': location
#         }
#         extracted_data.append(details)

#     return extracted_data


