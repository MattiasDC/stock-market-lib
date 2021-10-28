
class Factory:
	def __init__(self):
		self.creator_map = {}

	def register(self, name, creator):
		assert name not in self.creator_map, str((self.creator_map, name))
		self.creator_map[name] = creator

	def create(self, config):
		assert config['name'] in self.creator_map, str((self.creator_map, config["name"]))
		return self.creator_map[config.pop('name')](config)