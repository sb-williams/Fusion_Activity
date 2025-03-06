"""This is to manage datetime as well as the flexibility of Pandas"""

import pandas as pd
import shutil
import glob
import oracle_actions
import send_message


def process_file(src_path):
    # Load the file into a dataframe for processing (ETL)
    df = pd.read_excel(src_path)

    # If the dataframe is empty or corrupt, then kill the process and send an error message.
    if df.empty:
        return False

    # Once the file is loaded and there are no issues, we can go ahead and archive it
    print("Processing File")
    source_dir = r"\\esbmft01\ESB_Fusion\INBOUND\Tableau\Login"
    pattern = "*.xlsx"
    destination_dir = r"\\esbmft01\ESB_Fusion\INBOUND\Tableau\Login\archive"
    file_match = glob.glob(source_dir + "\\" + pattern)
    for file in file_match:
        shutil.move(file, destination_dir)
    
    
    # The file has 2 columns: USERNAME and DD
    # We need to split the DD column into 2 distinct columns: ACTIVITY_DATE and ACTIVITY_TIME

    # First, Set DD to the proper Datetime data type and remove the "T" time seperator
    df["DD"] = pd.to_datetime(df["DD"]).dt.tz_convert("US/Central")
    df['ACTIVITY_DATE'] = df["DD"].dt.date
    df['ACTIVITY_TIME'] = df["DD"].dt.time
    # Reorder the dataframe to match the table layout in Oracle. (Mapping)
    df = df.reindex(
        [
            "USERNAME",
            "ACTIVITY_DATE",
            "ACTIVITY_TIME",
            "DD",
        ],
        axis=1,
    )

    # Save data to Oracle table
    data_load = oracle_actions.backup_data(df)

    # Lets check the data to see if there is any activity between 9PM and 5AM and
    # use any records found to send an email to the ERP team.
    max_activity_time = pd.DataFrame({'startrange': ['1904-01-01 09:00:00 PM']})
    max_activity_time['startrange'] = pd.to_datetime(max_activity_time['startrange'])
    max_activity_time['ACTIVITY_TIME'] = max_activity_time['startrange'].dt.time

    min_activity_time = pd.DataFrame({'startrange': ['1904-01-01 05:00:00 AM']})
    min_activity_time['startrange'] = pd.to_datetime(min_activity_time['startrange'])
    min_activity_time['ACTIVITY_TIME'] = min_activity_time['startrange'].dt.time
    
    range_max_test = max_activity_time['ACTIVITY_TIME']
    range_min_test = min_activity_time['ACTIVITY_TIME']
    
    # Create an empty list to build our activity email if needed. We will use it
    # in the for loop below to build out a display of detected activity in our email body
    activity_data = []

    for index, row in df.iterrows():
        if df["ACTIVITY_TIME"][index] > range_max_test[0] or df['ACTIVITY_TIME'][index] < range_min_test[0]:
            activity_data.append(row)
            
    if len(activity_data) == 0:
        is_activity = False
        body = f"No after hours activity."
        # Now we can send out our email message
        send_message.send_message(is_activity,'Suspicious Fusion User Activity', body)
        return True
    else:
        # create a new dataframe from the list and pass it as part of the email function
        is_activity = True
        after_hours_data = pd.DataFrame(activity_data)
        # Drop the full datetime field from the message as it is not needed.
        after_hours_data.drop("DD", axis=1, inplace=True)
        # Build the body of the message
        body = f"{after_hours_data.to_html(index=False, justify="center")}"

        # Now we can send out our email message
        send_message.send_message(is_activity,'Suspicious Fusion User Activity', body)
        return True
