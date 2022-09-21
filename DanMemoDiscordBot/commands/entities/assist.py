class Assist:
    def __init__(self, name="", skills=[], instant_effects=[]):
        """(self, list of skil effects, bool) -> Assist
        skills: non mlb skill effects or mlb skill effects
        """
        self.name = name
        self.skills = skills
        self.instant_effects = instant_effects
        self.total_activations = 0
        self.current_turn_activations = 0

    @property
    def max_activations(self) -> int:
        for skill in self.skills:
            if skill.attribute == "instant_effect":
                return int(skill.duration.replace("+", ""))
        raise ValueError("Unit is missing duration on instant effect")

    @property
    def activations_per_turn(self) -> int:
        for skill in self.skills:
            if skill.attribute == "instant_effect":
                return int(skill.maxActivations or 1)
        raise ValueError("Unit is missing max_activations on instant effect")
