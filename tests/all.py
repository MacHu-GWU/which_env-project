# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from which_env.tests import run_cov_test

    run_cov_test(
        __file__,
        "which_env",
        is_folder=True,
        preview=False,
    )
