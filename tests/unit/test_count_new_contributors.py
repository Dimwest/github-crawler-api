import pandas as pd
from tests.unit.data import test_count_input, test_count_expected
from chalicelib.crawler import count_new_contributors


def test_count_new_contributors():

    assert (
        pd.DataFrame.to_dict(count_new_contributors(test_count_input))
        == test_count_expected
    )
