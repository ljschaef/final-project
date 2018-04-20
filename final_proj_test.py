# Lucas Schaefer - ljschaef
# Final Project SI 206
# Test File

from final_proj import *
import unittest

class TestClassBuilder(unittest.TestCase):

    # Now have function definitions in here of random tests

    def fuck_testing(self):

        fighter = Fighter(name='Lucas Schaefer', fight_name='Schaefdaddy', age=20,
                          height='6\'4"', weight=185, record='2-5-0', reach=76,
                          leg_reach=40)
        self.assertEqual(fighter.name, 'Lucas Schaefer')
        self.assertEqual(fighter.fightname, 'Schaefdaddy')
        self.assertEqual(fighter.age, 20)
        self.assertEqual(fighter.height, '6\'4"')
        self.assertEqual(fighter.weight, 185)
        self.assertEqual(fighter.record, '2-5-0')
        self.assertEqual(fighter.reach, 76)
        self.assertEqual(fighter.legreach, 40)

        fighter2 = Fighter(name='Jessica Zhang', fight_name='JZ', age=20,
                           height='5\'4"', weight=132, record='4-1-0', reach=64,
                           leg_reach=28)
        self.assertEqual(fighter2.name, 'Jessica Zhang')
        self.assertEqual(fighter2.fightname, 'JZ')
        self.assertEqual(fighter2.age, 20)
        self.assertEqual(fighter2.height, '5\'4"')
        self.assertEqual(fighter2.weight, 132)
        self.assertEqual(fighter2.record, '4-1-0')
        self.assertEqual(fighter2.reach, 64)
        self.assertEqual(fighter2.legreach, 28)

unittest.main()
