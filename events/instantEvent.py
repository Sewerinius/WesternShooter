class InstantEvent:
    def __init__(self, entity, attribute, targetValue, checkMethod, effects):
        self.entity = entity
        self.attribute = attribute
        self.targetValue = targetValue
        self.checkMethod = checkMethod
        self.effects = effects

    def run(self, data, camera):
        if self.checkMethod(getattr(self.entity, self.attribute), self.targetValue):
            return self.loop(data, camera)
        else:
            return False

    def loop(self, data, camera):
        for effect in self.effects:
            effect.run()
        return True
