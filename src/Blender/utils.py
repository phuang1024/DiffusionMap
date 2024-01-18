def get_name_res(filename: str):
    """
    Ground012_1K-JPG -> ("Ground012", 1)
    """
    name = filename.split("_")[0]
    res = int(filename.split("_")[1].split("-")[0][:-1])
    return name, res
