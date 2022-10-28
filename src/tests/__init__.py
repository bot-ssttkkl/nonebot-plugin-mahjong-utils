import pytest


class MyTest:
    env = {}

    @pytest.fixture(autouse=True)
    def set_env(self, monkeypatch):
        for key, value in self.env.items():
            monkeypatch.setenv(key, str(value))
        print("set env")

    @pytest.fixture(autouse=True)
    def load_plugin(self, set_env, nonebug_init):
        import nonebot  # 这里的导入必须在函数内

        # 加载插件
        nonebot.load_plugin("nonebot_plugin_mahjong_utils")
        print("load plugin")
