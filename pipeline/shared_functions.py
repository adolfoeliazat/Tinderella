def clean_file_lst(file_name_lst, jpg=False):
    """
    input: list of file/directory file names
    output: cleaned list consisting of only jpg files
    and non-hidden directories.
    """
    if not jpg:
        return [fname for fname in file_name_lst if not fname.startswith('.')]
    elif jpg:
        return [fname for fname in file_name_lst if '.jpg' in fname]
