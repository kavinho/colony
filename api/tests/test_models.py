# import pdb # pdb.set_trace()
import unittest
from v1.models import Person
import json

class TestPerson(unittest.TestCase):

    def test_person_tags(self):
        tags = ["id", "quis"]

        person = Person(_id='1',
                        index=1,
                        tags = tags
                        )

        self.assertEqual(person._tags, json.dumps(tags))
        self.assertEqual(len(person.tags), 2)

    def test_person_friends(self):
        friends = [{"index": 0},
                   {"index": 1}
                   ]

        person = Person(_id='1',
                        index=1,
                        friends = friends
                        )

        self.assertEqual(person._friends, json.dumps(friends))
        self.assertEqual(len(person.friends), 2)

    def test_person_diet_break_down(self):

        favouriteFood = ["apple",
                   "cucumber",
                   "strawberry"]

        person = Person(_id='1',
                        index=1,
                        age=20,
                        name='alo',
                        favouriteFood = favouriteFood
                        )

        self.assertEqual(person._favourite_food, json.dumps(favouriteFood))
        self.assertEqual(len(person.favourite_food), 3)
        diet = person.get_diet()
        self.assertEqual(diet['age'],20)
        self.assertEqual(diet['username'],'alo')
        self.assertEqual(len(diet['vegetables']),1)
        self.assertEqual(len(diet['fruits']),2)

    def test_common_friends(self):

        person1 = Person(_id='1',
                        index=1,
                        friends = [{"index": 0},{"index": 1}]
                       )

        person2 = Person(_id='2',
                        index=2,
                        friends = [{"index": 1},{"index": 3}]
                       )

        self.assertEqual(len(person1.get_common_friends_indexes(person2)),1)
        self.assertEqual(len(person2.get_common_friends_indexes(person1)),1)
        self.assertEqual(person1.get_common_friends_indexes(person2)[0],1)
