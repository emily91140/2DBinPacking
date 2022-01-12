
class BRKGA():
    def __init__(self, data, num_generations = 200, p = 100, p_elite = 100*0.25, p_mutant = 100*0.1, elite_inheritance_prob = 0.8):
        self.data = data # 排程輸入資料

        # Configuration
        self.num_generations = num_generations # num of generation
        self.p = p # size of population
        self.p_elite = p_elite # size of elite population
        self.p_mutant = p_mutant # size of mutant population
        self.elite_inheritance_prob = elite_inheritance_prob # elite allel inheritance prob




