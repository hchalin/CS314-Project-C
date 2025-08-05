class StarMap:
    def __init__(self, planets, target, artifacts):
        self.planets = planets
        self.target = target
        self.artifacts = artifacts

    def display(self):
        print("Displaying StarMap:")
        print("Planets:", self.planets)
        print("Target:", self.target)
        print("Artifacts:", self.artifacts)