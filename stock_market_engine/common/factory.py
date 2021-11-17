
class Factory:
	def __init__(self):
		self.creator_map = {}

	def register(self, name, creator):
		assert name not in self.creator_map, str((self.creator_map, name))
		self.creator_map[name] = creator
		return self

	def create(self, name, config):
		assert name in self.creator_map, str((self.creator_map, name))
		return self.creator_map[name](config)