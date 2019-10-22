import loader


class SpawnEntity:
    def __init__(self, entities):
        self.entities = entities

    def run(self):
        loader.data.entities += self.entities