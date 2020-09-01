import unittest
import json
from app import app
from unittest.mock import MagicMock
from v1.models import Person

class BasicTestCase(unittest.TestCase):

    def get_app(self):
        storage = MagicMock()
        app.config['storage'] =storage
        return app

    def test_employees(self):
        the_app = self.get_app()
        the_app.config['storage'].get_company_employees.return_value = [ Person(_id='123', index=1,name='joe'),
                                                                     Person(_id='456', index=2, name='joe-2')
                                                                   ]

        tester = the_app.test_client(self)
        response = tester.get('/v1/company/1/employees', content_type='application/json')
        employees = json.loads(response.data)['employees']

        self.assertEqual(response.status_code, 200)
        the_app.config['storage'].get_company_employees.ensure_called_wtih('1')
        self.assertEqual(employees[0]['_id'], '123')
        self.assertEqual(employees[1]['_id'], '456')
        # todo storage called with arg 1

    def test_get_people_diet(self):

        the_app = self.get_app()
        favourite_food = ["apple",
                   "cucumber",
                   "strawberry"]

        the_app.config['storage'].get_person.return_value = Person(_id='123',
                                                                   index=1,
                                                                   name='joe',
                                                                   favouriteFood=favourite_food
                                                               )
        tester = the_app.test_client(self)
        response = tester.get('v1/people/1/diet', content_type='application/json')

        data = json.loads(response.data)
        the_app.config['storage'].get_person.ensure_called_wtih('1')
        self.assertEqual(data.get('fruits',[]),['apple', 'strawberry'])
        self.assertEqual(data.get('vegetables',[]),['cucumber'])

    def test_common_friends(self):

        the_app = self.get_app()
        person1 = Person(_id='1',
                         index=1,
                         friends = [{"index": 0},{"index": 3}]
                        )

        person2 = Person(_id='2',
                         index=2,
                         friends = [{"index": 3},{"index": 4}]
                        )

        common_friend = Person(_id='3',
                               index=3,
                               friends = [{"index": 1},{"index": 2}, {"index": 5}]
                              )

        the_app.config['storage'].get_person.side_effect = [person1, person2]
        the_app.config['storage'].get_people.return_value =[common_friend]

        tester = the_app.test_client(self)
        response = tester.get('v1/people/1/common_friends_with?other_index=2',
                              content_type='application/json')
        commons = json.loads(response.data).get('commons')

        self.assertEqual(len(commons),1)
        self.assertTrue(the_app.config['storage'].get_person.call_args_list, [('1'), ('2')])
        the_app.config['storage'].get_people.assert_called_with(indexes=[3])

