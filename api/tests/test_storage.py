import unittest
import mock
from storage import SQLStorage
from v1.models import Person

class TestStorage(unittest.TestCase):

    def test_get_company_employees(self):
        # ------- prepare
        session_mock = mock.MagicMock()
        storage = SQLStorage(session_mock)
        # ------- action
        storage.get_company_employees(1)
        # ------- assert
        session_mock.query.called_with(Person)
        session_mock.query.return_value.filter.assert_called()
        expected = Person.company_id ==1
        actual = session_mock.query.return_value.filter.call_args.args[0]

        self.assertTrue((expected.compare(actual)))

    def test_get_person(self):

        # ------- prepare
        session_mock = mock.MagicMock()
        storage = SQLStorage(session_mock)
        # ------- action
        storage.get_person(1)
        # ------- assert
        session_mock.query.called_with(Person)
        session_mock.query.return_value.filter.assert_called()
        expected = Person.index == 1
        actual = session_mock.query.return_value.filter.call_args.args[0]

        self.assertTrue((expected.compare(actual)))

    def test_clear_data(self):

        # ------- prepare
        session_mock = mock.MagicMock()
        storage = SQLStorage(session_mock)
        # ------- action
        storage.clear_data()
        # ------- assert
        # self.client.query(Person).delete()
        self.assertNotEqual(str(session_mock.query.mock_calls) ,
                            "[call(<class 'api.models.Person'>),call().delete()," +
                            "call(<class 'api.models.Company'>),call().delete()]")

    def test_add_data(self):

        # ------- prepare
        session_mock = mock.MagicMock()
        storage = SQLStorage(session_mock)
        # ------- action
        storage.save(Person())
        # ------- assert
        self.assertTrue('call.add(<v1.models.Person object' in str(session_mock.mock_calls[0]))

        self.assertEqual(str(session_mock.mock_calls[1]),'call.commit()')
