from mfapi.mutual_fund_data import MutualFundData
from util.file_utils import FileUtils

if __name__ == "__main__":
    # for i in range(5):
    #     properties = FileUtils.get_properties()
    #     print(properties)
    # mfd = MutualFundData()
    # mfd.get_historic_data_for_given_scheme("120716")
    mutual_funds_list = FileUtils.get_mutual_funds_list()

    mfd = MutualFundData()
    mutual_funds_scheme_code = mfd.get_scheme_codes_for_given_mutual_funds(mutual_funds_list)
    for mutual_fund in mutual_funds_list:
        mfd.get_historic_data_for_given_scheme(mutual_funds_scheme_code[mutual_fund])
