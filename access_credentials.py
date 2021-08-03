# function to get the access credentials from an inpdut file and form an api endpoint
import windstream_logger

logging = windstream_logger.get_logger("access_credentials")

import os
import pandas as pd

region_code_list = ["US", "SA", "AF", "AP", "AU", "CA", "EU"]


def access_credentials():

    checkFile = ".\input_file.xlsx"
    if os.path.isfile(checkFile):

        # print("yes the file is there")
        logging.info("yes the file is the specified path")
    
        input_df = pd.read_excel(checkFile, sheet_name="input_config_2", index_col=None)

        for index, row in input_df.iterrows():

            try:
                org_id = int(row["org_id"])
                # print(org_id)
                logging.info(org_id)
                region_code = row["region_code"]
                logging.info(region_code)
                if region_code == "" or region_code not in region_code_list:
                    logging.error(
                        "Region code is empty or not valid, moving forward with next row"
                    )
                    continue

                else:
                    logging.info(
                        "The org id" + str(int(org_id)) + "region-code" + region_code
                    )
                    url_with_region_code = (
                        "https://apis-" + region_code + ".highbond.com/v1/"
                    )
                    # forming the base base_url for api call
                    base_url = url_with_region_code + "orgs/" + str(org_id)
                    logging.info(base_url)
                    input_df.loc[index, "base_url"] = base_url
                    logging.info(input_df)

            except ValueError:

                input_df = input_df.dropna()
                # print(str(row["org_id"]), "This is not a number. Please enter a valid number")
                logging.error(
                    str(row["org_id"])
                    + "This is not a number. Please enter a valid number"
                )
                continue
    else:

        print("Input file not found in the specified path, please check the path")
        logging.critical(
            "Input file not found in the specified path, please check the path"
        )
        exit()

    return input_df
