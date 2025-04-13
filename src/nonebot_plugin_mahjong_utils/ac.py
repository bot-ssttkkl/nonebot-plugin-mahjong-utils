from nonebot_plugin_access_control_api.service import SubService, create_plugin_service

plugin_service = create_plugin_service("nonebot_plugin_mahjong_utils")

sniffer_service: SubService = plugin_service.create_subservice("sniffer")
command_service: SubService = plugin_service.create_subservice("command")
