import rookies
import veterans
import rmse
import sys
sys.path.append("../../data_generation/.")
import normalization
import baseline
import oracle


stats = ['2PAPM', '2PP', '2PPM', '3PAPM', '3PAr', '3PP', '3PPM', 'ASTP', 'ASTPM', 'BLKP', 'BLKPM', 'BPM', 'DBPM', 'DRBP', 'DRBPM', 'DWSPM', 'FGAPM', 'FGP', 'FGPM', 'FTAPM', 'FTP', 'FTPM', 'FTr', 'G', 'GS', 'GSPG', 'MP', 'MPG', 'OBPM', 'ORBP', 'ORBPM', 'OWSPM', 'PER', 'PFPM', 'PPM', 'STLP', 'STLPM', 'TOVP', 'TOVPM', 'TRBP', 'TRBPM', 'TSP', 'USGP', 'VORP', 'WSP48', 'WSPM', 'eFGP']


# baseline/oracle
print "computing baseline and oracle"
baseline_results = baseline.compute_baseline()
oracle_results = oracle.compute_oracle()

# compute results
print "starting rookie results"
rookie_baseline_2 = baseline_results["rookies"]
rookie_results_2 = rookies.get_rookie_comparison(data_type=2, validation_trials=10)
rookie_oracle_2 = oracle_results["rookies"]
print "finished rookie results"

print "starting veteran results"
veteran_baseline_2 = baseline_results["veterans"]
veteran_results_2 = veterans.get_veteran_comparison(data_type=2)
veteran_oracle_2 = oracle_results["veterans"]
print "finished veteran results"

# remove value normalization
print "undoing normalization"
rookie_baseline_2 = normalization.unnormalize_baseline(rookie_baseline_2, outliers_removed=False, normalization="-1to1")
rookie_results_2 = normalization.unnormalize(rookie_results_2, outliers_removed=False, normalization="-1to1")
rookie_oracle_2 = normalization.unnormalize_baseline(rookie_oracle_2, outliers_removed=False, normalization="-1to1")

veteran_baseline_2 = normalization.unnormalize_baseline(veteran_baseline_2, outliers_removed=False, normalization="-1to1")
veteran_results_2 = normalization.unnormalize(veteran_results_2, outliers_removed=False, normalization="-1to1", training=True)
veteran_oracle_2 = normalization.unnormalize_baseline(veteran_oracle_2, outliers_removed=False, normalization="-1to1")
print "finished unnormalizing"

# regularization output
'''
fout = open("regularization.csv", "a")
fout.write("validation, ")
for stat in stats:
    fout.write(str(rmse.compute_rmse(veteran_results_2["validation"]["true"][stat], veteran_results_2["validation"]["predicted"][stat])) + ", ")
fout.write("\n")
fout.close()
''' 

# print output
print (" ,  rookie_baseline, rookie_validation, rookie_test, rookie_oracle, veteran_baseline, veteran_training, veteran_validation, veteran_test, veteran_oracle, \n")
for stat in stats:
    print (str(stat) + ", "
           + str(rmse.compute_rmse(rookie_baseline_2["true"][stat], rookie_baseline_2["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(rookie_results_2["validation"]["true"][stat], rookie_results_2["validation"]["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(rookie_results_2["test"]["true"][stat], rookie_results_2["test"]["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(rookie_oracle_2["true"][stat], rookie_oracle_2["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(veteran_baseline_2["true"][stat], veteran_baseline_2["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(veteran_results_2["training"]["true"][stat], veteran_results_2["training"]["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(veteran_results_2["validation"]["true"][stat], veteran_results_2["validation"]["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(veteran_results_2["test"]["true"][stat], veteran_results_2["test"]["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(veteran_oracle_2["true"][stat], veteran_oracle_2["predicted"][stat])) + ", ")

# file output
print "file output"
fout = open("stats_results.csv", "w")

fout.write(" ,  rookie_baseline, rookie_validation, rookie_test, rookie_oracle, veteran_baseline, veteran_training, veteran_validation, veteran_test, veteran_oracle, \n")
for stat in stats:
    fout.write(str(stat) + ", "
           + str(rmse.compute_rmse(rookie_baseline_2["true"][stat], rookie_baseline_2["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(rookie_results_2["validation"]["true"][stat], rookie_results_2["validation"]["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(rookie_results_2["test"]["true"][stat], rookie_results_2["test"]["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(rookie_oracle_2["true"][stat], rookie_oracle_2["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(veteran_baseline_2["true"][stat], veteran_baseline_2["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(veteran_results_2["training"]["true"][stat], veteran_results_2["training"]["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(veteran_results_2["validation"]["true"][stat], veteran_results_2["validation"]["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(veteran_results_2["test"]["true"][stat], veteran_results_2["test"]["predicted"][stat])) + ", "
           + str(rmse.compute_rmse(veteran_oracle_2["true"][stat], veteran_oracle_2["predicted"][stat])) + ", \n")

# type of normalization did not appear to make a difference 
'''
# and 0,1,3,4..., this is an example of 5
#rookie_results_5 = rookies.get_rookie_comparison(data_type=5)
#veteran_results_5 = veterans.get_veteran_comparison(data_type=5)
#rookie_results_5 = normalization.unnormalize(rookie_results_2, outliers_removed=True, normalization="0to1")
#veteran_results_5 = normalization.unnormalize(veteran_results_2, outliers_removed=True, normalization="0to1")
'''
'''
fout.write(" ,  , no_norm_outliers, no_norm_no_outliers, -1to1_outliers, -1to1_no_outliers, 0to1_outliers, 0to1_no_outliers, \n")
for stat in stats:
    print stat
     
    fout.write(str(stat) + ", ")
    fout.write("rookie_validation, ")
    #fout.write(str(rmse.compute_rmse(rookie_results_0["validation"]["true"][stat], rookie_results_0["validation"]["predicted"][stat])) + ", ")
    #fout.write(str(rmse.compute_rmse(rookie_results_1["validation"]["true"][stat], rookie_results_1["validation"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(rookie_results_2["validation"]["true"][stat], rookie_results_2["validation"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(rookie_results_3["validation"]["true"][stat], rookie_results_3["validation"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(rookie_results_4["validation"]["true"][stat], rookie_results_4["validation"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(rookie_results_5["validation"]["true"][stat], rookie_results_5["validation"]["predicted"][stat])) + ", ")
    fout.write("\n")
     
    fout.write(str(stat) + ", ")
    fout.write("rookie_test, ")
    #fout.write(str(rmse.compute_rmse(rookie_results_0["test"]["true"][stat], rookie_results_0["test"]["predicted"][stat])) + ", ")
    #fout.write(str(rmse.compute_rmse(rookie_results_1["test"]["true"][stat], rookie_results_1["test"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(rookie_results_2["test"]["true"][stat], rookie_results_2["test"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(rookie_results_3["test"]["true"][stat], rookie_results_3["test"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(rookie_results_4["test"]["true"][stat], rookie_results_4["test"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(rookie_results_5["test"]["true"][stat], rookie_results_5["test"]["predicted"][stat])) + ", ")
    fout.write("\n")

    fout.write(str(stat) + ", ")
    fout.write("veteran_validation, ")
    #fout.write(str(rmse.compute_rmse(veteran_results_0["validation"]["true"][stat], veteran_results_0["validation"]["predicted"][stat])) + ", ")
    #fout.write(str(rmse.compute_rmse(veteran_results_1["validation"]["true"][stat], veteran_results_1["validation"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(veteran_results_2["validation"]["true"][stat], veteran_results_2["validation"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(veteran_results_3["validation"]["true"][stat], veteran_results_3["validation"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(veteran_results_4["validation"]["true"][stat], veteran_results_4["validation"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(veteran_results_5["validation"]["true"][stat], veteran_results_5["validation"]["predicted"][stat])) + ", ")
    fout.write("\n")

    fout.write(str(stat) + ", ")
    fout.write("veteran_test, ")
    #fout.write(str(rmse.compute_rmse(veteran_results_0["test"]["true"][stat], veteran_results_0["test"]["predicted"][stat])) + ", ")
    #fout.write(str(rmse.compute_rmse(veteran_results_1["test"]["true"][stat], veteran_results_1["test"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(veteran_results_2["test"]["true"][stat], veteran_results_2["test"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(veteran_results_3["test"]["true"][stat], veteran_results_3["test"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(veteran_results_4["test"]["true"][stat], veteran_results_4["test"]["predicted"][stat])) + ", ")
    fout.write(str(rmse.compute_rmse(veteran_results_5["test"]["true"][stat], veteran_results_5["test"]["predicted"][stat])) + ", ")
    fout.write("\n")

fout.close()
'''
