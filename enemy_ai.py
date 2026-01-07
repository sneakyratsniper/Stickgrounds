import pygame
import random
from attacks import ATTACKS


class EnemyAI:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.state = "IDLE"
        self.state_timer = 0

    def state_action(self):
        player, enemy = self.player, self.enemy

        if self.state == "IDLE":
            pass

        if self.state in ("CHASE", "RETREAT", "ATTACK"):
            direction = 1 if player.rect.x > enemy.rect.x else -1
            if self.state == "RETREAT":
                direction *= -1

            if (
                not enemy.dashing
                and (
                    random.randint(1, 10) <= 1
                    or (enemy.hit and random.randint(1, 10) <= 2)
                )
            ):
                enemy.dash_timer = enemy.current_time

            enemy.rect.x += direction * enemy.speed

            if abs(player.rect.centerx - enemy.rect.centerx) <= 5:
                enemy.ai_state = self.state = "IDLE"
                enemy.dashing = False
                enemy.dash_cooldown += 1

            enemy.rect.x = max(0, min(1080, enemy.rect.x))

        if self.state == "BLOCK":
            pass

        if not enemy.is_attacking:
            if self.state in ("CHASE", "RETREAT"):
                enemy.update_action(1)
            else:
                enemy.update_action(0)

            if self.state == "ATTACK":
                enemy.attack_type = random.choice(["punch", "kick"])
                if ATTACKS[enemy.attack_type].combo_attack:
                    enemy.combo = random.choice([True, False])

                enemy.ai_state = self.state = "CHASE"

    def state_cooldown(self):
        if self.state_timer >= 0.35:
            self.state_timer -= 1
        else:
            self.state = self.choose_state()
            self.enemy.ai_state = self.state
            self.state_timer = random.randint(0, 0)

    def choose_state(self):
        distance = abs(self.player.rect.x - self.enemy.rect.x)

        scores = {
            "BLOCK": 0.0,
            "CHASE": 0.0,
            "ATTACK": 0.0,
            "RETREAT": 0.0,
            "IDLE": 0.0,
        }

        # 0 = never, 1 = almost certain
        state_votes = {k: [] for k in scores}

        if self.player.is_attacking:
            state_votes["BLOCK"].append(0.4 if distance < 120 else 0.1)
            state_votes["RETREAT"].append(0.5 if distance < 120 else 0.3)
            state_votes["ATTACK"].append(0.3 if distance < 120 else 0.0)

        if self.enemy.block_break:
            state_votes["RETREAT"].append(0.8)

        if self.enemy.hp < 40:
            state_votes["RETREAT"].append(0.2)
            state_votes["BLOCK"].append(0.1)

        if distance > 250:
            state_votes["CHASE"].append(0.8)

        elif distance > 120:
            state_votes["ATTACK"].append(0.2)
            state_votes["CHASE"].append(0.4)
            state_votes["RETREAT"].append(0.05)
            state_votes["IDLE"].append(0.05)

            if (
                self.player.hp < 40
                or self.player.block_break
                or self.player.blocking
                or self.player.hit
                or self.enemy.ult_active
            ):
                state_votes["CHASE"].append(0.4)
        else:
            state_votes["ATTACK"].append(0.9)
            state_votes["RETREAT"].append(0.05)
            state_votes["BLOCK"].append(0.05)

            if (
                self.player.hp < 40
                or self.player.block_break
                or self.player.blocking
                or self.player.hit
                or self.enemy.ult_active
            ):
                state_votes["ATTACK"].append(0.8)
            else:
                state_votes["RETREAT"].append(0.15)
                state_votes["BLOCK"].append(0.15)

        for k, votes in state_votes.items():
            if votes:
                scores[k] = combine_confidences(votes)
            else:
                scores[k] = 0.1

        return random.choices(list(scores.keys()), weights=scores.values())[0]

    def update(self):
        self.enemy.ai_state = self.state
        self.state_action()
        self.state_cooldown()


def combine_confidences(votes):
    product = 1.0
    for v in votes:
        product *= (1 - v)
    return 1 - product
