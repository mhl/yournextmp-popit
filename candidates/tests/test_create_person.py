from django.test import TestCase

from mock import patch, MagicMock

from .fake_popit import (
    fake_get_result,
    FakePersonCollection, FakeOrganizationCollection
)
from .helpers import equal_call_args
from ..views import PersonUpdateMixin, CandidacyMixin, PopItApiMixin

class MinimalUpdateClass(PersonUpdateMixin, CandidacyMixin, PopItApiMixin):
    pass

class TestCreatePerson(TestCase):

    @patch.object(FakePersonCollection, 'post')
    @patch('candidates.views.requests')
    @patch('candidates.popit.PopIt')
    def test_create_jane_doe(self, mock_popit, mock_requests, mocked_post):

        mocked_post.return_value = {
            'result': {
                'id': 'jane-doe'
            }
        }

        mock_requests.get = fake_get_result

        mock_popit.return_value.organizations = FakeOrganizationCollection
        mock_popit.return_value.persons = FakePersonCollection

        view = MinimalUpdateClass()

        view.create_candidate_list_memberships = MagicMock()
        view.create_party_memberships = MagicMock()

        new_person_data = {
            "birth_date": None,
            "email": "jane@example.org",
            "gender": "female",
            "homepage_url": "http://janedoe.example.org",
            "identifiers": [
                {
                    "scheme": "yournextmp-candidate",
                    "identifier": "1234567"
                }
            ],
            "name": "Jane Doe",
            "party_memberships": {
                "2015": {
                    "id": "party:53",
                    "name": "Labour Party"
                }
            },
            "standing_in": {
                "2015": {
                    "mapit_url": "http://mapit.mysociety.org/area/65808",
                    "name": "Dulwich and West Norwood"
                }
            },
            "twitter_username": "",
            "wikipedia_url": "",
            "facebook_personal_url": "http://notreallyfacebook/tessajowell",
            "facebook_page_url": "http://notreallyfacebook/tessajowellcampaign",
            "party_ppc_page_url": "http://labour.example.org/tessajowell",
        }

        view.create_person(
            new_person_data,
            {
                'information_source': 'A change made for testing purposes',
                'username': 'tester',
                'version_id': '6054aa38b30b4418',
                'timestamp': '2014-09-28T14:02:44.567413',
            },
        )

        expected_args = {
            'birth_date': None,
            'email': u'jane@example.org',
            'gender': 'female',
            'id': '1',
            'identifiers': [
                {
                    'scheme': 'yournextmp-candidate',
                    'identifier': '1234567'
                }
            ],
            'links': [
                {
                    'note': 'facebook page',
                    'url': 'http://notreallyfacebook/tessajowellcampaign',
                },
                {
                    'note': 'party PPC page',
                    'url': 'http://labour.example.org/tessajowell',
                },
                {
                    'note': 'facebook personal',
                    'url': 'http://notreallyfacebook/tessajowell',
                },
                {
                    'note': 'homepage',
                    'url': 'http://janedoe.example.org'
                },
            ],
            'name': u'Jane Doe',
            'party_memberships': {
                '2015': {
                    'id': 'party:53',
                    'name': 'Labour Party'
                }
            },
            'standing_in': {
                '2015': {
                    'name': 'Dulwich and West Norwood',
                    'mapit_url': 'http://mapit.mysociety.org/area/65808'}
            },
            'versions': [
                {
                    'information_source': 'A change made for testing purposes',
                    'username': 'tester',
                    'version_id': '6054aa38b30b4418',
                    'timestamp': '2014-09-28T14:02:44.567413',
                    'data': {
                        'twitter_username': '',
                        'standing_in': {
                            '2015': {
                                'name': 'Dulwich and West Norwood',
                                'mapit_url': 'http://mapit.mysociety.org/area/65808'
                            }
                        },
                        'homepage_url': 'http://janedoe.example.org',
                        'identifiers': [
                            {
                                'scheme': 'yournextmp-candidate',
                                'identifier': '1234567'
                            }
                        ],
                        'facebook_page_url': 'http://notreallyfacebook/tessajowellcampaign',
                        'facebook_personal_url': 'http://notreallyfacebook/tessajowell',
                        'party_ppc_page_url': 'http://labour.example.org/tessajowell',
                        'birth_date': None,
                        'gender': 'female',
                        'name': 'Jane Doe',
                        'wikipedia_url': '',
                        'party_memberships': {
                            '2015': {
                                'id': 'party:53',
                                'name': 'Labour Party'
                            }
                        },
                        'email': 'jane@example.org',
                        'id': '1'
                    }
                }
            ],
        }

        # Then we expect one post, with the right data:
        self.assertEqual(1, len(mocked_post.call_args_list))
        self.assertTrue(
            equal_call_args(
                [expected_args],
                mocked_post.call_args[0]
            ),
            "update_person was called with unexpected values"
        )

        view.create_candidate_list_memberships.assert_called_once_with(
            'jane-doe',
            new_person_data,
        )
        view.create_party_memberships.assert_called_once_with(
            'jane-doe',
            new_person_data
        )
