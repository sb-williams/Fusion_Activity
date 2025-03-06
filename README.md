# Fusion_Activity

This is a Python project used to help the Oracle Fusion team monitor fraud activity.

It is a simple project that takes a daily extract of user activity via a csv file. The program detects the creation of the file.
Once detected, the file is loaded into a Pandas dataframe and put through a simple ETL process.

The data is stored to an Oracle table. If there is fraud activity detected, an email with the details is sent to the fusion team.
