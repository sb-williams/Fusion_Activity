import os
from dotenv import load_dotenv
import pandas as pd
import oracledb

def backup_data(df):

    print("Updating Tables")
    load_dotenv()

    # d = r"C:\\Oracle32\\product\\19.0.0\\client_1\\instantclient"
    # oracledb.init_oracle_client(lib_dir=d)

    # Connect to a database using the env variable
    conn_test = oracledb.connect(
        user=os.environ.get("DATA_KEY"),
        password=os.environ.get("DATA_SECRET"),
        host=os.environ.get("DATA_HOST"),
        port=os.environ.get("DATA_PORT"),
        service_name=os.environ.get("SERVICE_NAME"),
    )

    conn_prod = oracledb.connect(
        user=os.environ.get("DATA_KEY"),
        password=os.environ.get("DATA_SECRET"),
        host=os.environ.get("DATA_HOST2"),
        port=os.environ.get("DATA_PORT2"),
        service_name=os.environ.get("SERVICE_NAME"),
    )
    

    # If the connection fails, cancel the update and send a failure message.
    if not conn_test or not conn_prod:
        return False
    else:
        # Lets make a deep copy of our df so we can modify the colums data type to match the table.
        df2 = df.copy()
        # Set the format of the copy time field to be a time-stamp type
        df2["ACTIVITY_TIME"] = pd.to_datetime(df2["ACTIVITY_TIME"], format='%H:%M:%S')

        # A cursor is used to send SQL actions to the table
        cursor_test = conn_test.cursor()
        cursor_prod = conn_prod.cursor()

        # Append the data from the dataframe to the table
        rows = [tuple(x) for x in df2.values]
        cursor_test.executemany(
            "INSERT INTO FIN_USER_ACTIVITY VALUES (:1,:2,:3,:4)",
            rows,
        )
        cursor_prod.executemany(
            "INSERT INTO FIN_USER_ACTIVITY VALUES (:1,:2,:3,:4)",
            rows,
        )

        # Save the appended records to the table.
        conn_test.commit()
        conn_prod.commit()

        # Close the connection and cursor to the table and database for security reasons.
        cursor_test.close()
        cursor_prod.close()
        conn_test.close()
        conn_prod.close()

        return True
