import csv

def add_separator(input, separator):
    if input.endswith(separator[0]):
        return input[:-1] + separator + ' '
    return input + separator + ' '

def format(input, separator, prefix = None):
    # Remove errant whitespace
    input = input.strip()
    # If this column is empty, return a null string
    if input == None or len(input) == 0:
        return ''
    # Add a prefix to the start of the input, if supplied
    if prefix:
        input = prefix + ' ' + input
    # Add a separator to the end of the input, if necessary
    if separator:
        return add_separator(input, separator)
    return input

def format_serial_details(row):
    output = ''
    serial_details = [
        format(row.get('volume'), None, 'т.'),
        format(row.get('issue'), None, 'вып.'),
        format(row.get('number'), None, '№'),
        format(row.get('part'), None, 'ч.'),
        format(row.get('book'), None, 'кн.'),
        format(row.get('section'), None, 'отд.'),
        format(row.get('pagination'), None, 'паг.'),
        row.get('date'),
    ]
    return ', '.join(list(filter(None, serial_details))).capitalize()

def format_pages(row):
    output = ''
    pages = [
        format(row.get('pages'), None),
        format(row.get('additional_issue'), None),
    ]
    return ' ; '.join(list(filter(None, pages)))

# If the first character of the input string is lowercase, this function returns
# the value. Otherwise, it returns None.
def only_if_lowercase(input, value):
    if not input:
        return None
    if input[0].isupper():
        return None
    return value

with open('test.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row.get('id'):
            print()
        output = ''
        if row.get('article_title').strip().startswith('То же') or row.get('book_title').strip().startswith('То же'):
            output += ''
        else:
            output += format(row.get('id'), '.')
        output += format(row.get('authors'), '.')
        if row['type'] == 'journal_article' or row['type'] == 'newspaper_article' or row['type'] == 'collection_article':
            output += format(row.get('article_title'), ' //')
        output += format(row.get('book_title'), '. —')
        output += format(row.get('place'), ' :' if row.get('publisher') else ',')
        output += format(row.get('publisher'), ',')
        output += format(row.get('year'), '. —')
        output += format(format_serial_details(row), '. —')
        output += format(format_pages(row), '. —')
        if row.get('bibliography'):
            bibliography_prefix = 'Библиогр.' + (':' if row.get('bibliography').startswith('с.') else '')
            output += format(row.get('bibliography'), '. —', bibliography_prefix)
        output += format(row.get('resume'), '. —', only_if_lowercase(row.get('resume'), 'Рез.'))
        output += format(row.get('series'), '. —')
        output += format(row.get('signature'), '. —', 'Подп.')

        # Remove em dash and space at end of string
        if output.endswith('— '):
            output = output[:-len('— ')]
        print(output)

        if row.get('annotation'):
            print(format(row.get('annotation'), '.'))
