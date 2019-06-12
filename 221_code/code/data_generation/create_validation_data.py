import pickle

fnames = ["data.pkl", "data_removeoutliers.pkl", "data_-1to1.pkl", "data_-1to1_removeoutliers.pkl", "data_0to1.pkl", "data_0to1_removeoutliers.pkl"]

for fname in fnames:

    fin = open(fname, "rb")
    data = pickle.load(fin)
    fin.close()

    # remove 2017-18 seasons, remove players with only 2017-18 season
    for player in data.keys():
        # remove players with only 2017-18 season
        if len(data[player]["professional"].keys()) == 1 and "2017-18" in data[player]["professional"].keys():
            del data[player]
        # remove 2017-18 season
        elif "2017-18" in data[player]["professional"].keys():
            del data[player]["professional"]["2017-18"]

    fout = open(fname[:-4] + "_validation.pkl", "wb")
    pickle.dump(data, fout)
    fout.close()
