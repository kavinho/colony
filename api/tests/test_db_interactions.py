# import pdb # pdb.set_trace()
import unittest
import os
from app import app
from v1.models import Company, Person

class TestInsertLoad(unittest.TestCase):
    """
    This is a brief test to demo the concept, of testing each unit.
    Testing save and insert, select models.

    """

    @classmethod
    def tearDownClass(cls):
        import pathlib
        current_dir = pathlib.Path(__file__).parent.absolute()
        dest_file = os.path.join(current_dir,  'paranuara_test.db')
        try:
            os.remove(dest_file)
        except OSError:
            pass

    def test_company_create_read(self):

        db_session = app.config['storage'].client
        company = Company(index=100,company='test-company')
        db_session.add(company)
        db_session.commit()
        loaded_company = app.config['storage'].client.query(Company).filter(Company.id == 100).first()
        self.assertEqual(company.name , loaded_company.name, 'created and loaded models.Company are not identical')

    def test_person_create_read(self):

        db_session = app.config['storage'].client
        created_person = Person(_id="595eeb9b96d80a5bc7afb106",
                                index=1,
                                guid="5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
                                has_died=False,
                                balance="$2,418.59",
                                picture="http://placehold.it/32x32",
                                age= 61,
                                eyeColor= "blue",
                                name="Carmella Lambert")

        db_session.add(created_person)
        db_session.commit()
        loaded_person = app.config['storage'].client.query(Person).filter(Person.index == 1).first()

        self.assertEqual(created_person.name,
                         loaded_person.name,
                         'created and loaded models.Person are not identical')

