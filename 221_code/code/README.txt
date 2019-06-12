There are two directories, algorithm and data_generation.

In data_generation, web_scraper.py will generate CSVs by downloading data from basketball-reference.com.  data_structure.py will take those CSVs and form them into .pkl files that the algorithm will later load in Python (each .pkl file is normalized differently but is same data).

Alternatively, you could just move the files in data.zip into the data_generation folder and then run data_structure.py.

In algorithm, there are two directories, games and stats.  stats is for statisical projetion.  Running run.py will run the projection, with the results being printed and written to the stats-results.csv file.  In games, running predict.py will run 100 trials of game prediction with the results being printed to the screen.
