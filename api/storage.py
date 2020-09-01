from v1.models import Company, Person

class Storage(object):
    """
        Base class to abstract away databse interaction details.
    """


    def get_company_employees(self,index):
        pass

    def get_people(self, indexes):
        pass

    def get_person(self, index):
        pass

    def clear_data(self):
        pass

    def save(self, model_instance):
        pass


class SQLStorage(Storage):

    def __init__(self, client):
        self.client = client

    def get_company_employees(self,index):
        return self.client.query(Person).filter(Person.company_id ==index)

    def get_person(self, index):
        return self.client.query(Person).filter( Person.index == index).first()

    def get_people(self, indexes):
        return self.client.query(Person).filter(Person.index.in_(indexes)).all()

    def clear_data(self):
        self.client.query(Person).delete()
        self.client.query(Company).delete()

        self.client.commit()

    def save(self, model_instance):

        self.client.add(model_instance)
        self.client.commit()
