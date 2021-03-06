from django.conf.urls import patterns, include, url

from django.contrib import admin

from candidates.views import (ConstituencyPostcodeFinderView,
    ConstituencyNameFinderView, ConstituencyDetailView, CandidacyView,
    CandidacyDeleteView, NewPersonView, UpdatePersonView, RevertPersonView,
    PersonView, HelpApiView, HelpAboutView, ConstituencyListView)

urlpatterns = patterns('',
    url(r'^$', ConstituencyPostcodeFinderView.as_view(), name='finder'),
    url(r'^lookup/name$', ConstituencyNameFinderView.as_view(), name='lookup-name'),
    url(r'^lookup/postcode$', ConstituencyPostcodeFinderView.as_view(), name='lookup-postcode'),
    url(r'^constituencies$', ConstituencyListView.as_view(), name='constituencies'),
    url(r'^constituency/(?P<mapit_area_id>\d+)/(?P<ignored_slug>.*)$',
        ConstituencyDetailView.as_view(),
        name='constituency'),
    url(r'^candidacy$',
        CandidacyView.as_view(),
        name='candidacy-create'),
    url(r'^candidacy/delete$',
        CandidacyDeleteView.as_view(),
        name='candidacy-delete'),
    url(r'^person/create/$',
        NewPersonView.as_view(),
        name='person-create'),
    url(r'^person/(?P<person_id>.*)/update$',
        UpdatePersonView.as_view(),
        name='person-update'),
    url(r'^person/(?P<person_id>.*)/revert$',
        RevertPersonView.as_view(),
        name='person-revert'),
    url(r'^person/(?P<person_id>.*)$',
        PersonView.as_view(),
        name='person-view'),
    url(r'^help/api', HelpApiView.as_view(), name='help-api'),
    url(r'^help/about', HelpAboutView.as_view(), name='help-about'),
    url(r'^admin/', include(admin.site.urls)),
)
