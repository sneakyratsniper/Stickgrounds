class Attack:
  def __init__(self,name,damage,block_damage,animation,animation_speed,hit_frame,size,displacement=0,combo_attack="",combo_frames=(0,0)):
    self.name = name
    self.damage = damage
    self.block_damage = block_damage
    self.animation = animation
    self.animation_speed = animation_speed
    self.hit_frame = hit_frame
    self.size = size 

    self.displacement = displacement
    self.combo_attack = combo_attack
    self.combo_frames = combo_frames



ATTACKS = {
    #"name": Attack("name",damage,block_damage,animation,animation_speed,hit_frame,combo_attack,combo_frames)
    "punch": Attack("punch", 5, 20, 2, 1.0, 8, (80,50), combo_attack="punch_2", combo_frames=(9,16)),
    "punch_2": Attack("punch_2", 5, 20, 3, 1.0, 13, (90,50),displacement=20),
    "kick": Attack("kick", 7, 50, 4, 0.8, 19, (120,75)),
}
