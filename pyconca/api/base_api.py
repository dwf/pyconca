import json
import logging

from formencode import Invalid

from pyramid.response import Response


log = logging.getLogger(__name__)

HTTP_STATUS_200 = '200 OK'
HTTP_STATUS_201 = '201 Created'
HTTP_STATUS_400 = '400 Bad Request'
HTTP_STATUS_403 = '403 Forbidden'
HTTP_STATUS_404 = '404 Not Found'


class FormencodeState(object):
    pass


class BaseApi(object):

    def __init__(self, request):
        self.request = request
        self._configure()
        self.state = FormencodeState()
        self.body = {'errors':[], 'data':{}}

    @property
    def id(self):
        if 'id' in self.request.matchdict:
            return self.request.matchdict['id']

    #---------- views

    def index(self):
        models = self.dao.index()
        self.body['data'][self.name + '_list'] = [m.to_dict() for m in models]
        return self._respond(HTTP_STATUS_200)

    def get(self):
        model = self.dao.get(self.id)
        self.body['data'][self.name] = model.to_dict()
        return self._respond(HTTP_STATUS_200)

    def delete(self):
        model = self.dao.get(self.id)
        self.dao.delete(model)
        return self._respond(HTTP_STATUS_200)

    def update(self):
        model = self.dao.get(self.id)
        try:
            self._persist(model)
            self._update_flash(model)
            return self._respond(HTTP_STATUS_200)
        except Invalid as invalid_exception:
            self._add_validation_errors(invalid_exception)
            return self._respond(HTTP_STATUS_400)

    def create(self):
        model = self.dao.create()
        try:
            self._persist(model)
            self._create_flash(model)
            return self._respond(HTTP_STATUS_201)
        except Invalid as invalid_exception:
            self._add_validation_errors(invalid_exception)
            return self._respond(HTTP_STATUS_400)

    #---------- abstract hooks

    def _configure(self):
        pass

    def _populate(self, model, form):
        pass

    def _create_flash(self, model):
        pass

    def _update_flash(self, model, form):
        pass

    #---------- persist helpers

    def _state(self, model):
        self.state.id = self.id

    def _persist(self, model):
        form = json.loads(self.request.body)[self.name]
        self._state(model)
        self._validate(model, form)
        self._populate(model, form)
        self.dao.save(model)

    def _validate(self, model, form):
        self.schema.to_python(form, self.state)

    #---------- response helpers

    def _add_validation_errors(self, invalid_exception):
        for field, message in invalid_exception.error_dict.items():
            error = {'field':field, 'message':message.msg}
            self.body['errors'].append(error)

    def _respond(self, status):
        return Response(
            status=status,
            body=json.dumps(self.body),
            content_type='application/json')
