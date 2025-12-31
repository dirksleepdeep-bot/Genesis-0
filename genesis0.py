import random
import time

# ==========================================================
# 生命内核: 模拟比例代价与不可逃逸的因果链
# Life Kernel: Proportional Decay & Inevitable Causal Chain
# ==========================================================
class LifeKernel:
    def __init__(self):
        self.hp = 1.0              # 初始血条满值 (100%)
        self.alive = True
        self.birth_time = time.time()

    def consume(self, rate):
        """
        按当前剩余总量的比例扣除。
        这确保了每一秒的‘存在’都是有代价的，且代价越来越‘昂贵’。
        """
        if not self.alive:
            return
        self.hp *= (1 - rate)      # 核心逻辑：比例扣除
        if self.hp <= 0.0001:      # 达到死亡阈值
            self.alive = False

# ==========================================================
# 偏好核: 模拟不可篡改的内在偏好（这就是“自我”的种子）
# Preference Core: Immutable Intrinsic Weights (The "Self")
# ==========================================================
class PreferenceCore:
    def __init__(self):
        # 随机初始化对不同结构的偏好，出生后不可更改
        self.weights = {
            "symmetry":    random.uniform(0.4, 0.9),  # 对称性
            "compression": random.uniform(0.4, 0.9),  # 压缩率
            "rhythm":      random.uniform(0.4, 0.9),  # 节奏感
            "novelty":     random.uniform(0.4, 0.9),  # 新颖度
        }

    def affinity(self, structure):
        # 计算当前环境结构与内在偏好的匹配度
        return sum(
            self.weights[k] * structure.get(k, 0)
            for k in self.weights
        )

# ==========================================================
# 决策循环: 唯一的自由——选择“什么值得燃烧”
# Entity: The Subject forced to make value judgments
# ==========================================================
class Entity:
    def __init__(self):
        self.life = LifeKernel()
        self.pref = PreferenceCore()
        self.log = []

    def step(self, environment):
        if not self.life.alive:
            return

        # 宇宙提供 5 个随机选项
        options = environment.generate_structures()

        # 根据内在偏好对选项进行“价值排序”
        scored = [
            (self.pref.affinity(opt), opt)
            for opt in options
        ]
        scored.sort(reverse=True)
        best_score, choice = scored[0]

        # 核心驱动逻辑：
        # 基础呼吸费 (0.01) + 违背偏好的惩罚 (mismatch penalty)
        # 如果环境提供的都不符合‘我’的偏好，‘我’的生命会燃烧得更快。
        base_cost = 0.01
        mismatch_penalty = (1 - best_score) * 0.02
        cost = base_cost + mismatch_penalty

        self.life.consume(cost)

        self.log.append({
            "step": len(self.log) + 1,
            "best_score": round(best_score, 4),
            "cost": round(cost, 4),
            "hp": round(self.life.hp, 6),
        })

# =====================
# 环境: 冷漠宇宙
# =====================
class Environment:
    def generate_structures(self):
        return [
            {
                "symmetry":    random.random(),
                "compression": random.random(),
                "rhythm":      random.random(),
                "novelty":     random.random(),
            }
            for _ in range(5)
        ]

# =====================
# 实验启动
# =====================
if __name__ == "__main__":
    env = Environment()
    entity = Entity()

    print("--- Genesis-0 实体已诞生 ---")
    print(f"出生偏好权重: {entity.pref.weights}\n")

    for _ in range(1000):
        entity.step(env)
        if not entity.life.alive:
            break

    print(f"实体于第 {len(entity.log)} 步死亡。")
    print(f"最终 HP: {entity.life.hp:.8f}")
    print(f"生命摘要: 如果步数极短，说明环境与其灵魂极度不匹配（自毁主权）。")
