import pandas as pd

class SchemeUtils:
    @staticmethod
    def generate_scheme_summary(scheme_name, scheme_code, fifty_two_week_high, today_gain_loss_from_52_week_high):
        """
        Generates a DataFrame with scheme summary information.

        Args:
            scheme_name: Name of the scheme.
            scheme_code: Code of the scheme.
            fifty_two_week_high: 52-week high of the scheme's NAV.
            today_gain_loss_from_52_week_high: Today's gain/loss from 52-week high.

        Returns:
            A pandas DataFrame containing the scheme summary.
        """

        # Convert gain/loss string to float (remove '%' and convert to float)
        today_gain_loss_from_52_week_high = float(today_gain_loss_from_52_week_high.strip('%'))

        data = {
            'Scheme_Name': scheme_name,
            'Scheme_Code': scheme_code,
            '52_Week_High': fifty_two_week_high,
            'Current_Gain_Loss_From_52_Week_High_In_Percentage': today_gain_loss_from_52_week_high,
        }
        return pd.DataFrame([data])
