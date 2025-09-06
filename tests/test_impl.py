# -*- coding: utf-8 -*-

import os
import pytest

from which_runtime.api import Runtime
from which_env.impl import (
    USER_ENV_NAME,
    ENV_NAME,
    EnvNameValidationError,
    validate_env_name,
    CommonEnvNameEnum,
    BaseEnvNameEnum,
    detect_current_env,
)


class EnvNameEnum(BaseEnvNameEnum):
    devops = CommonEnvNameEnum.devops.value
    dev = CommonEnvNameEnum.dev.value
    tst = CommonEnvNameEnum.tst.value
    prd = CommonEnvNameEnum.prd.value


def test_validate_env_name():
    valid_names = [
        "dev",
        "devops",
        "prd",
        "tst",
        "stg",
        "qa",
        "sbx",
        "sbx1",
        "sbx123",
        "test1",
        "env2",
    ]
    for name in valid_names:
        validate_env_name(name)  # Should not raise

    invalid_names = ["1dev", "9test", "0env"]
    for name in invalid_names:
        with pytest.raises(
            EnvNameValidationError, match="first letter of env_name has to be a-z"
        ):
            validate_env_name(name)

    invalid_names = [
        "dev-1",
        "test_env",
        "dev.1",
        "env@1",
        "test env",
        "dev/1",
        "env-test",
    ]
    for name in invalid_names:
        with pytest.raises(
            EnvNameValidationError, match="env_name can only has a-z, 0-9"
        ):
            validate_env_name(name)


class TestBaseEnvNameEnum:
    """
    Test the built-in ``EnvNameEnum`` class.
    """

    def test_good_validation(self):
        EnvNameEnum.validate()

    def test_missing_required_env_validation(self):
        class Enum1(BaseEnvNameEnum):
            devops = CommonEnvNameEnum.devops.value

        with pytest.raises(ValueError):
            Enum1.validate()

        class Enum2(BaseEnvNameEnum):
            dev = CommonEnvNameEnum.dev.value
            prd = CommonEnvNameEnum.prd.value

        with pytest.raises(ValueError):
            Enum2.validate()

    def test_invalid_env_name_validation(self):
        class Enum3(BaseEnvNameEnum):
            devops = CommonEnvNameEnum.devops.value
            dev = CommonEnvNameEnum.dev.value
            prd = CommonEnvNameEnum.prd.value
            first = "1"

        with pytest.raises(EnvNameValidationError):
            Enum3.validate()

    def test_get_xyz(self):
        assert EnvNameEnum.get_devops() == EnvNameEnum.devops.value
        assert EnvNameEnum.get_dev() == EnvNameEnum.dev.value
        assert EnvNameEnum.get_prd() == EnvNameEnum.prd.value

    def test_get_workload_env_list(self):
        assert EnvNameEnum.get_workload_env_list() == [
            EnvNameEnum.dev.value,
            EnvNameEnum.tst.value,
            EnvNameEnum.prd.value,
        ]

    def test_emoji(self):
        for env_name in EnvNameEnum:
            _ = env_name.emoji
            # print(f"{env_name.value} = {env_name.emoji}")


class TestDetectCurrentEnv:
    """Test environment detection function."""

    def setup_method(self):
        """Clean environment variables before each test."""
        if USER_ENV_NAME in os.environ:
            del os.environ[USER_ENV_NAME]
        if ENV_NAME in os.environ:
            del os.environ[ENV_NAME]

    def teardown_method(self):
        """Clean environment variables after each test."""
        if USER_ENV_NAME in os.environ:
            del os.environ[USER_ENV_NAME]
        if ENV_NAME in os.environ:
            del os.environ[ENV_NAME]

    def test_local_runtime_default_to_dev(self):
        """Test local runtime defaults to dev environment."""
        mock_runtime = Runtime()
        mock_runtime.is_local_runtime_group = True
        mock_runtime.is_ci_runtime_group = False
        mock_runtime.is_app_runtime_group = False
        mock_runtime.is_glue_container = False

        result = detect_current_env(EnvNameEnum, mock_runtime)
        assert result == "dev"

    def test_ci_runtime_with_env_name(self):
        """Test CI runtime uses ENV_NAME."""
        mock_runtime = Runtime()
        mock_runtime.is_local_runtime_group = False
        mock_runtime.is_ci_runtime_group = True
        mock_runtime.is_app_runtime_group = False
        mock_runtime.is_glue_container = False

        os.environ[ENV_NAME] = "prd"
        result = detect_current_env(EnvNameEnum, mock_runtime)
        assert result == "prd"

    def test_ci_runtime_user_env_priority(self):
        """Test CI runtime prioritizes USER_ENV_NAME over ENV_NAME."""
        mock_runtime = Runtime()
        mock_runtime.is_local_runtime_group = False
        mock_runtime.is_ci_runtime_group = True
        mock_runtime.is_app_runtime_group = False
        mock_runtime.is_glue_container = False

        os.environ[ENV_NAME] = "prd"
        os.environ[USER_ENV_NAME] = "tst"
        result = detect_current_env(EnvNameEnum, mock_runtime)
        assert result == "tst"


if __name__ == "__main__":
    from which_env.tests import run_cov_test

    run_cov_test(
        __file__,
        "which_env.impl",
        preview=False,
    )
