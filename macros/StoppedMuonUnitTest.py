import pandas as pd
import unittest

# Define a custom unit test class
class DataFrameTest(unittest.TestCase):

    def test_exclude_events(self):
        # Sample data for df_prestop
        df_prestop = pd.DataFrame({'EventID': [1, 2, 3, 4, 5],
                                   'Data': ['A', 'B', 'C', 'D', 'E']})

        # Sample data for df_poststop
        df_poststop = pd.DataFrame({'EventID': [3, 4],
                                    'Data': ['C', 'D']})

        # Expected result
        expected_result = pd.DataFrame({'EventID': [1, 2, 5],
                                        'Data': ['A', 'B', 'E']})

        # Create a new DataFrame with events from df_prestop excluding events in df_poststop
        df_new = df_prestop[~df_prestop['EventID'].isin(df_poststop['EventID'])].copy()

        print(df_new)

        # Reset the indices of both DataFrames
        expected_result.reset_index(drop=True, inplace=True)
        df_new.reset_index(drop=True, inplace=True)

        # Assert the resulting DataFrame matches the expected result
        pd.testing.assert_frame_equal(df_new, expected_result)

# Run the unit tests
if __name__ == '__main__':
    unittest.main()
