import json
from flask import request, Blueprint, current_app
from werkzeug.utils import secure_filename
from .models import Company, Person
import os

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/company/<index>/employees')
def get_company_employees(index):
    storage = current_app.config['storage']

    response ={'success':True, 'employees':[]}
    for item in storage.get_company_employees(index):
        response['employees'].append(item.to_dict_full_info())

    return response

@api_v1.route('/people/<index>/diet')
def get_people_diet(index):

    storage = current_app.config['storage']
    person = storage.get_person(index)
    if person:
        return person.get_diet()
    else:
        return {
            'error': 'NOT_FOUND',
            'details': 'No person found with index {}'.format(index)
        }


@api_v1.route('/people/<index>/common_friends_with')
def get_people_common_friends(index):

    if index is None:
        return {'error': 'MISSING_ARG',
                'details':'expected to find index argument'}

    other_index = request.args.get('other_index',None)

    if index is None:
        return {'error': 'MISSING_ARG',
                'details':'expected to find other_index argument'}


    storage = current_app.config['storage']
    person_1 = storage.get_person(index)
    person_2 = storage.get_person(other_index)

    if person_1 is None:
        return {'error': 'NOT_FOUND',
                'details':'Could not find anyone with index {}'.format(index)}

    if person_2 is None:
        return {'error': 'NOT_FOUND',
                'details':'Could not find anyone with index {}'.format(other_index)}
    indexes = person_1.get_common_friends_indexes(person_2)
    friends = storage.get_people(indexes= indexes)

    return {
       'commons': [frnd.to_dict_full_info() for frnd in friends]
    }

# ----------db  maintenance ---------------

@api_v1.route('/upload/companies',methods=['POST'])
def upload_companies():

    upload_folder =  current_app.config['UPLOAD_FOLDER']
    result  = handle_upload(request , upload_folder)

    if result.get('success',False):
        upload_to_storage(result['path'],current_app.config['db_session'],Company)

    return {'success': True}

@api_v1.route('/upload/people',methods=['POST'])
def upload_people():
    upload_folder =  current_app.config['UPLOAD_FOLDER']
    result  = handle_upload(request , upload_folder)

    if result.get('success',False):
        upload_to_storage(result['path'],current_app.config['db_session'],Person)

    return {'success': True}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()=='json'


def upload_to_storage(source_file, db_session, klass):

    with open(source_file) as json_file:
        items = json.load(json_file)

    for item in items:
        try:
            instance = klass(**item)
            db_session.add(instance)
            db_session.commit()
        except Exception as e:
            current_app.logger.error(msg='error', e=e)

def handle_upload(upload_request, upload_folder):

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in upload_request.files:
            return {'result': False, 'reason': 'No file part'}

        file = upload_request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename

        if file.filename == '':
            return {'success': False, 'reason': 'No selected file'}


        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path)
            return {'path':save_path,'success': True}

@api_v1.route('/clear_data',methods=['POST'])
def clear_data():
    storage = current_app.config['storage']
    storage.clear_data()
    return json.dumps({'success':True}), 200, {'ContentType': 'application/json'}
