import json

from django import http
from django.views.generic import FormView
from django.core.paginator import InvalidPage
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse, resolve
from django.utils.functional import LazyObject


class MoreCapableJsonEncoder(json.JSONEncoder):
    """
    Two issues.

    We need to support Django's LazyObject.

    We need to support Money and Decimal objects
    """

    def default(self, o):
        if isinstance(o, LazyObject):
            # urgh, that's going to bite us at some point
            o._setup()
            return o._wrapped
        else:
            return json.JSONEncoder.default(self, o)


def JsonResponse(data, status_code=200, cache_age=None, json_encoder_instance=None):
    "A factory function that encodes the data into a HttpResponse."

    if json_encoder_instance:
        response_data = json_encoder_instance.encode(data)
    else:
        response_data = json.dumps(data, cls=MoreCapableJsonEncoder)

    response = http.HttpResponse(response_data, content_type="application/json")
    response.status_code = status_code
    response['Access-Control-Allow-Origin'] = "*"
    response['Access-Control-Allow-Headers'] = "Authorization"
    if cache_age:
        response['Cache-Control'] = "max-age=%i" % cache_age
    return response


class AjaxTemplateMixin(object):
    """ Vary the template on request.is_ajax.
    TODO: Also attempt to call ajax_get() etc instead of the usual
    ones if they are present?
    """
    def dispatch(self, request, **kwargs):
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, **kwargs)


class AjaxLoadMoreMixin(object):
    """ Mixin for providing AJAX pagination facilities to any
    view that takes a "page" kwarg and provides a "page" variable in it's context data
    """
    def get(self, request, **kwargs):
        response = super(AjaxLoadMoreMixin, self).get(request, **kwargs)
        if request.is_ajax():
            json_data = {"content": response.render().content}

            try:
                next_page = response.context_data["page_obj"].next_page_number()
                if next_page:
                    kwargs = dict(self.kwargs)
                    kwargs["page"] = next_page
                    try:
                        json_data["next_url"] = reverse(resolve(request.path).url_name, args=self.args, kwargs=kwargs)
                    except NoReverseMatch:
                        # this results in there not being a Next button
                        json_data["next_url"] = None
            except InvalidPage:
                pass
            # response = JsonResponse(json, status_code=200)
        return response


class AjaxFormView(FormView):
    FORM_INVALID_HTTP_STATUS_CODE = 400
    '''
    A specialised version of the Django FormView that provides default
    JSON responses for AJAX requests.
    '''

    def form_valid(self, form):
        '''
        Calls the appropriate handler depending on whether or not we're
        dealing with an AJAX request. If you would subclass this when
        using a normal FormView, you should subclass default_form_valid
        or ajax_form_valid instead.
        '''
        if self.request.is_ajax():
            return self.ajax_form_valid(form)
        else:
            return self.default_form_valid(form)

    def ajax_form_valid(self, form):
        '''
        Handles AJAX submissions with valid data by responding with a
        200 (OK) with a JSON body.
        '''
        return JsonResponse(
            {'result': 'ok'},
            status_code=200,
        )

    def default_form_valid(self, form):
        '''
        Handles non-AJAX submissions with valid data by calling FormView's
        implemenation of form_valid.
        '''
        return super(AjaxFormView, self).form_valid(form)

    def form_invalid(self, form):
        '''
        Calls the appropriate handler depending on whether or not we're
        dealing with an AJAX request. If you would subclass this when
        using a normal FormView, you should subclass default_form_invalid
        or ajax_form_invalid instead.
        '''
        if self.request.is_ajax():
            return self.ajax_form_invalid(form)
        else:
            return self.default_form_invalid(form)

    def ajax_form_invalid(self, form):
        '''
        Handles AJAX submissions with invalid data and responds with a
        400 (bad request) with a JSON body containing errors and the form's
        prefix.
        '''
        return JsonResponse(
            {
                'result': 'error',
                'errors': form.errors,
                'prefix': form.add_prefix(''),
            },
            status_code=self.FORM_INVALID_HTTP_STATUS_CODE,
        )

    def default_form_invalid(self, form):
        '''
        Handles non-AJAX submissions with invalid data by calling FormView's
        implementation of form_invalid.
        '''
        return super(AjaxFormView, self).form_invalid(form)


class AjaxFormDataView(AjaxFormView):
    FORM_INVALID_HTTP_STATUS_CODE = 200

    def get_form_kwargs(self):
        if not self.request.is_ajax():
            return super(AjaxFormDataView, self).get_form_kwargs()
        form_kwargs = super(AjaxFormDataView, self).get_form_kwargs()
        request_body = self.request.read()
        try:
            data = json.loads(request_body)
        except (ValueError, TypeError):
            data = {}
        form_kwargs['data'] = data
        return form_kwargs

