import pandas as pd

class MutualFundDashboard:
    def calculate_rolling_returns(self, nav_df, periods):
        """
        Calculates rolling returns for specified periods.

        Args:
            nav_df: DataFrame containing the NAV history.
            periods: List of periods for rolling returns (e.g., [1, 2, 3, 5, 10]).

        Returns:
            A dictionary of rolling returns for each period.
        """
        rolling_returns = {}
        for period in periods:
            nav_df['nav'] = pd.to_numeric(nav_df['nav'])
            rolling_returns[f'{period}'] = nav_df['nav'].pct_change(periods=period * 252).dropna() * 100
        return rolling_returns

    def calculate_52_week_high(self, nav_df):
        """
        Calculates the 52-week high of the NAV.

        Args:
            nav_df: DataFrame containing the NAV history.

        Returns:
            The 52-week high NAV.
        """
        return nav_df['nav'].rolling(window=252).max().iloc[-len(nav_df)+251]

    def calculate_loss_from_52_week_high(self, nav_df, loss_percentages):
        """
        Calculates NAV values for given loss percentages from 52-week high.

        Args:
            nav_df: DataFrame containing the NAV history.
            loss_percentages: List of loss percentages (e.g., [10, 15, 20]).

        Returns:
            A dictionary of NAV values for each loss percentage.
        """
        fifty_two_week_high = self.calculate_52_week_high(nav_df)
        loss_levels = {f'{loss}%': fifty_two_week_high * (1 - loss / 100) for loss in loss_percentages}
        return loss_levels

    def calculate_today_gain_loss_from_52_week_high(self, nav_df):
        """
        Calculates today's percentage gain/loss from 52-week high.

        Args:
            nav_df: DataFrame containing the NAV history.

        Returns:
            Percentage gain/loss from 52-week high.
        """
        length = len(nav_df)
        today_nav = float(nav_df['nav'].iloc[-length])
        fifty_two_week_high = self.calculate_52_week_high(nav_df)
        return ((today_nav - fifty_two_week_high) / fifty_two_week_high) * 100

    def calculate_index_performance(self, index_nav_df, scheme_nav_df):
        """
        Calculates percentage increase/decrease from the selected index.

        Args:
            index_nav_df: DataFrame containing the index NAV history.
            scheme_nav_df: DataFrame containing the scheme NAV history.

        Returns:
            Percentage increase/decrease from the index.
        """
        # Calculate cumulative returns
        index_cumulative_return = (index_nav_df['nav'].iloc[-1] / index_nav_df['nav'].iloc[0]) - 1
        scheme_cumulative_return = (scheme_nav_df['nav'].iloc[-1] / scheme_nav_df['nav'].iloc[0]) - 1
        return (scheme_cumulative_return - index_cumulative_return) * 100
