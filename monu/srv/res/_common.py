def digestify(doc, keyring=['ingredient', 'child', 'step']):
    if 'child' in doc:
        for child in doc['child']:
            digestify(child, keyring)
    for key in keyring:
        if key in doc:
            del doc[key]
