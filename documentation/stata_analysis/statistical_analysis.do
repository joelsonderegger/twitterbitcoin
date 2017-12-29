
***!!!starting STATA and importing the csv file with the twitter + bitcoin data (from this folder)***
 import delimited \\SV-MONK\UNISG-Rfolder$\10613370\Desktop\HSG_project_SoftEngineering\twitterbitcoin\data\nr_of_tweets_bpi_closing_price.csv

***creating a date variable (time2) based on the variable (time) which is intepreted as string by import***
gen double time2 = clock(time, "YMD hms")
format time2 %tcNN-DD-CCYY_HH:MM:SS
order time2, after(time)

***defining the variable time2 to be a time series with hourly grogress and specific format***
tsset time2, format(%tcNN-DD-CCYY_HH:MM:SS) delta(1 hours)

***Graphs of all 6 variables, run one by one***
twoway (tsline nr_of_tweets)
twoway (tsline df_nr_of_tweets)
twoway (tsline log_df_nr_of_tweets)
twoway (tsline bpi_closing_price)
twoway (tsline df_bpi_closing_price)
twoway (tsline log_df_bpi_closing_price)

***running Augmented Dickey-Fuller test for all string variables at lag 0*** 
dfuller nr_of_tweets, lags(0)
dfuller df_nr_of_tweets, lags(0)
dfuller log_df_nr_of_tweets, lags(0)
dfuller bpi_closing_price, lags(0)
dfuller df_bpi_closing_price, lags(0)
dfuller log_df_bpi_closing_price, lags(0)

***running the lag specification criteria for the 2 selected variables, with maximum on lags 7)***
varsoc df_nr_of_tweets df_bpi_closing_price, maxlag(7)

***running the var regression for the 2 selected variables, with recommended lag 2)
var df_nr_of_tweets df_bpi_closing_price, lags(1/1)

***running the granger causality test for the above regression***
vargranger

***installing the outger2 package for exporting results to LaTex***
ssc install outreg2
outreg2 using var_regression.tex, replace
