import json

from popit_api import PopIt
from slugify import slugify
import requests

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.generic import FormView, TemplateView

from .forms import PostcodeForm


def get_candidate_list_popit_id(constituency_name, year):
    """Return the PopIt organization ID for a constituency's candidate list

    >>> get_candidate_list_popit_id('Leeds North East', 2010)
    'candidates-2010-leeds-north-east'
    >>> get_candidate_list_popit_id('Ayr, Carrick and Cumnock', 2015)
    'candidates-2015-ayr-carrick-and-cumnock'
    """
    return 'candidates-{year}-{slugified_name}'.format(
        year=year,
        slugified_name=slugify(constituency_name),
    )


class ConstituencyFinderView(FormView):
    template_name = 'candidates/finder.html'
    form_class = PostcodeForm

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode']
        url = 'http://mapit.mysociety.org/postcode/' + postcode
        r = requests.get(url)
        if r.status_code == 200:
            mapit_result = r.json
            mapit_constituency_id = mapit_result['shortcuts']['WMC']
            mapit_constituency_data = mapit_result['areas'][str(mapit_constituency_id)]
            constituency_url = reverse(
                'constituency',
                kwargs={'constituency_name': mapit_constituency_data['name']}
            )
            return HttpResponseRedirect(constituency_url)
        else:
            error_url = reverse('finder')
            error_url += '?bad_postcode=' + urlquote(postcode)
            return HttpResponseRedirect(error_url)

    def get_context_data(self, **kwargs):
        context = super(ConstituencyFinderView, self).get_context_data(**kwargs)
        bad_postcode = self.request.GET.get('bad_postcode')
        if bad_postcode:
            context['bad_postcode'] = bad_postcode
        return context

class ConstituencyDetailView(TemplateView):
    template_name = 'candidates/constituency.html'

    def get_context_data(self, **kwargs):
        context = super(ConstituencyDetailView, self).get_context_data(**kwargs)

        constituency_name = kwargs['constituency_name']

        old_candidate_list_id = get_candidate_list_popit_id(constituency_name, 2010)

        api = PopIt(
            instance=settings.POPIT_INSTANCE,
            hostname=settings.POPIT_HOSTNAME,
            api_version='v0.1',
            user=settings.POPIT_USER,
            password=settings.POPIT_PASSWORD,
            append_slash=False,
        )

        old_candidate_list_data = api.organizations(old_candidate_list_id).get()

        context['candidates_2010'] = [
            api.persons(membership['person_id']).get()['result']
            for membership in old_candidate_list_data['result']['memberships']
        ]

        context['constituency_name'] = constituency_name

        return context