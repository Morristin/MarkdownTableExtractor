import json


class Settings:
	def __init__(self):
		with open('settings.json', 'r') as setting_file:
			self.settings: dict = json.load(setting_file)

	def __getattr__(self, item):
		return self.settings.__getitem__(item)

	def __getitem__(self, item):
		return self.settings.__getitem__(item)


settings = Settings()
