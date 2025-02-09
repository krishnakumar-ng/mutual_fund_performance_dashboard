from mfapi.mutual_fund_data import MutualFundData
from mfdashboard.mutual_fund_dashboard import MutualFundDashboard
from util.file_utils import FileUtils
from util.scheme_utils import SchemeUtils

def main():
    mf_data = MutualFundData()
    mf_dashboard = MutualFundDashboard()

    mutual_funds_list = FileUtils.get_mutual_funds_list()
    mutual_funds_scheme_code = mf_data.get_scheme_codes_for_given_mutual_funds(mutual_funds_list)

    scheme_summary_list = []
    for mutual_fund in mutual_funds_list:

        scheme_code = mutual_funds_scheme_code[mutual_fund]
        # index_code = 67890  # Replace with the index code

        scheme_details = mf_data.get_scheme_details(scheme_code)
        scheme_name = scheme_details['scheme_name']
        scheme_nav_df = mf_data.get_nav_history(scheme_code)

        # Get index NAV history (replace with your actual index API endpoint)
        # index_nav_df = mf_data.get_nav_history(index_code)

        # Calculate key metrics
        fifty_two_week_high = mf_dashboard.calculate_52_week_high(scheme_nav_df)
        today_gain_loss_from_52_week_high = mf_dashboard.calculate_today_gain_loss_from_52_week_high(scheme_nav_df)
        rolling_returns = mf_dashboard.calculate_rolling_returns(scheme_nav_df, [1, 2, 3, 5, 10])
        # loss_levels = mf_dashboard.calculate_loss_from_52_week_high(scheme_nav_df, [10, 15, 20])
        # index_performance = mf_dashboard.calculate_index_performance(index_nav_df, scheme_nav_df)

        # Print or display the results
        print(f"Scheme Name: {scheme_name}")
        print(f"Scheme Code: {scheme_code}")
        print(f"52 Week High: {fifty_two_week_high}")
        print(f"Current Gain/Loss from 52 Week High: {today_gain_loss_from_52_week_high:.2f}%")
        # for period, return_series in rolling_returns.items():
        #     last_return = return_series.iloc[-len(return_series)]
        #     print(f"{period} Year Return: {last_return:.2f}%")
        # print("Loss Levels:")
        # for loss_percentage, nav_value in loss_levels.items():
        #     print(f"{loss_percentage} Loss: {nav_value}")
        # print(f"Performance vs. Index: {index_performance:.2f}%")

        # Create a DataFrame to store the results
        summary_df = SchemeUtils.generate_scheme_summary(scheme_name, scheme_code, fifty_two_week_high, f"{today_gain_loss_from_52_week_high:.2f}%")
        scheme_summary_list.append(summary_df)

    FileUtils.save_summaries_to_excel(scheme_summary_list)
    FileUtils.save_summaries_to_csv(scheme_summary_list)


if __name__ == "__main__":
    main()
