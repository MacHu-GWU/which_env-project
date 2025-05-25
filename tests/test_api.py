# -*- coding: utf-8 -*-

from which_env import api


def test():
    _ = api
    _ = api.USER_ENV_NAME
    _ = api.ENV_NAME
    _ = api.EnvNameValidationError
    _ = api.validate_env_name
    _ = api.CommonEnvNameEnum
    _ = api.BaseEnvNameEnum
    _ = api.env_emoji_mapper
    _ = api.detect_current_env


if __name__ == "__main__":
    from which_env.tests import run_cov_test

    run_cov_test(
        __file__,
        "which_env.api",
        preview=False,
    )
