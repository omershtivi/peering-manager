from __future__ import unicode_literals

from django import forms

from .constants import COMMUNITY_TYPE_CHOICES, PLATFORM_CHOICES
from .models import (AutonomousSystem, Community, ConfigurationTemplate,
                     InternetExchange, PeeringSession, Router)
from peeringdb.models import PeerRecord
from utils.forms import (BootstrapMixin, CSVChoiceField, FilterChoiceField,
                         PasswordField, SlugField, YesNoField)


class CommentField(forms.CharField):
    """
    A textarea with support for GitHub-Flavored Markdown. Exists mostly just to
    add a standard help_text.
    """
    widget = forms.Textarea
    default_label = 'Comments'
    default_helptext = '<i class="fa fa-info-circle"></i> <a href="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet" target="_blank">GitHub-Flavored Markdown</a> syntax is supported'

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        label = kwargs.pop('label', self.default_label)
        help_text = kwargs.pop('help_text', self.default_helptext)
        super(CommentField, self).__init__(required=required,
                                           label=label, help_text=help_text,
                                           *args, **kwargs)


class TemplateField(forms.CharField):
    """
    A textarea dedicated for template. Exists mostly just to add a standard
    help_text.
    """
    widget = forms.Textarea
    default_label = 'Template'
    default_helptext = '<i class="fa fa-info-circle"></i> <a href="https://github.com/respawner/peering-manager/wiki/configuration_template" target="_blank">Jinja2 template</a> syntax is supported'

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        label = kwargs.pop('label', self.default_label)
        help_text = kwargs.pop('help_text', self.default_helptext)
        super(TemplateField, self).__init__(required=required,
                                            label=label, help_text=help_text,
                                            *args, **kwargs)


class AutonomousSystemForm(BootstrapMixin, forms.ModelForm):
    irr_as_set_peeringdb_sync = YesNoField(required=False, label='IRR AS-SET')
    ipv6_max_prefixes_peeringdb_sync = YesNoField(required=False,
                                                  label='IPv6 Max Prefixes')
    ipv4_max_prefixes_peeringdb_sync = YesNoField(required=False,
                                                  label='IPv4 Max Prefixes')
    comment = CommentField()

    class Meta:
        model = AutonomousSystem
        fields = ('asn', 'name', 'irr_as_set', 'irr_as_set_peeringdb_sync',
                  'ipv6_max_prefixes', 'ipv6_max_prefixes_peeringdb_sync',
                  'ipv4_max_prefixes', 'ipv4_max_prefixes_peeringdb_sync',
                  'comment',)
        labels = {
            'asn': 'ASN',
            'irr_as_set': 'IRR AS-SET',
            'ipv6_max_prefixes': 'IPv6 Max Prefixes',
            'ipv4_max_prefixes': 'IPv4 Max Prefixes',
            'comment': 'Comments',
        }
        help_texts = {
            'asn': 'BGP autonomous system number (32-bit capable)',
            'name': 'Full name of the AS',
        }


class AutonomousSystemCSVForm(forms.ModelForm):
    class Meta:
        model = AutonomousSystem

        fields = ('asn', 'name', 'irr_as_set', 'ipv6_max_prefixes',
                  'ipv4_max_prefixes', 'comment',)
        labels = {
            'asn': 'ASN',
            'irr_as_set': 'IRR AS-SET',
            'ipv6_max_prefixes': 'IPv6 Max Prefixes',
            'ipv4_max_prefixes': 'IPv4 Max Prefixes',
            'comment': 'Comments',
        }
        help_texts = {
            'asn': 'BGP autonomous system number (32-bit capable)',
            'name': 'Full name of the AS',
        }


class AutonomousSystemImportFromPeeringDBForm(BootstrapMixin, forms.Form):
    model = AutonomousSystem
    asn = forms.IntegerField(
        label='ASN', help_text='BGP autonomous system number (32-bit capable)')
    comment = CommentField()


class AutonomousSystemFilterForm(BootstrapMixin, forms.Form):
    model = AutonomousSystem
    q = forms.CharField(required=False, label='Search')
    asn = forms.IntegerField(required=False, label='ASN')
    name = forms.CharField(required=False, label='AS Name')
    irr_as_set = forms.CharField(required=False, label='IRR AS-SET')
    ipv6_max_prefixes = forms.IntegerField(
        required=False, label='IPv6 Max Prefixes')
    ipv4_max_prefixes = forms.IntegerField(
        required=False, label='IPv4 Max Prefixes')


class CommunityForm(BootstrapMixin, forms.ModelForm):
    comment = CommentField()

    class Meta:
        model = Community

        fields = ('name', 'value', 'type', 'comment',)
        labels = {
            'comment': 'Comments',
        }
        help_texts = {
            'value': 'Community (RFC1997) or Large Community (RFC8092)',
            'type': 'Ingress to tag received routes or Egress to tag advertised routes'
        }


class CommunityCSVForm(BootstrapMixin, forms.ModelForm):
    type = CSVChoiceField(choices=COMMUNITY_TYPE_CHOICES, required=False,
                          help_text='Ingress to tag received routes or Egress to tag advertised routes')

    class Meta:
        model = Community

        fields = ('name', 'value', 'type', 'comment',)
        labels = {
            'comment': 'Comments',
        }
        help_texts = {
            'value': 'Community (RFC1997) or Large Community (RFC8092)',
        }


class CommunityFilterForm(BootstrapMixin, forms.Form):
    model = Community
    q = forms.CharField(required=False, label='Search')
    name = forms.CharField(required=False, label='Name')
    value = forms.CharField(required=False, label='Value')
    type = forms.MultipleChoiceField(choices=COMMUNITY_TYPE_CHOICES,
                                     required=False)


class ConfigurationTemplateForm(BootstrapMixin, forms.ModelForm):
    template = TemplateField()

    class Meta:
        model = ConfigurationTemplate
        fields = ('name', 'template', 'comment',)
        labels = {
            'comment': 'Comments',
        }


class ConfigurationTemplateFilterForm(BootstrapMixin, forms.Form):
    model = ConfigurationTemplate
    q = forms.CharField(required=False, label='Search')
    name = forms.CharField(required=False, label='Name')


class InternetExchangeForm(BootstrapMixin, forms.ModelForm):
    slug = SlugField()
    check_bgp_session_states = forms.ChoiceField(
        required=False, label='Check For Peering Session States',
        help_text='If enabled, with a usable router, the state of peering sessions will be updated.',
        choices=((True, 'Yes'), (False, 'No'),), widget=forms.Select())
    comment = CommentField()

    class Meta:
        model = InternetExchange
        fields = ('peeringdb_id', 'name', 'slug', 'ipv6_address',
                  'ipv4_address', 'configuration_template', 'router',
                  'check_bgp_session_states', 'comment',)
        labels = {
            'peeringdb_id': 'PeeringDB ID',
            'ipv6_address': 'IPv6 Address',
            'ipv4_address': 'IPv4 Address',
            'comment': 'Comments',
        }
        help_texts = {
            'peeringdb_id': 'The PeeringDB ID for the IX connection (can be left empty)',
            'name': 'Full name of the Internet Exchange point',
            'ipv6_address': 'IPv6 Address used to peer',
            'ipv4_address': 'IPv4 Address used to peer',
            'configuration_template': 'Template for configuration generation',
            'router': 'Router connected to the Internet Exchange point',
        }


class InternetExchangePeeringDBForm(BootstrapMixin, forms.ModelForm):
    slug = SlugField()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(InternetExchangePeeringDBForm, self).__init__(*args, **kwargs)
        self.fields['peeringdb_id'].widget = forms.HiddenInput()

    class Meta:
        model = InternetExchange
        fields = ('peeringdb_id', 'name', 'slug',
                  'ipv6_address', 'ipv4_address',)
        labels = {
            'ipv6_address': 'IPv6 Address',
            'ipv4_address': 'IPv4 Address',
        }
        help_texts = {
            'name': 'Full name of the Internet Exchange point',
            'ipv6_address': 'IPv6 Address used to peer',
            'ipv4_address': 'IPv4 Address used to peer',
        }


class InternetExchangePeeringDBFormSet(forms.BaseFormSet):
    def clean(self):
        """
        Check if slugs are uniques accross forms.
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on
            # its own
            return

        slugs = []
        for form in self.forms:
            slug = form.cleaned_data['slug']
            if slug in slugs:
                raise forms.ValidationError(
                    'Internet Exchanges must have distinct slugs.')
            slugs.append(slug)


class InternetExchangeCSVForm(forms.ModelForm):
    slug = SlugField()

    class Meta:
        model = InternetExchange
        fields = ('name', 'slug', 'ipv6_address', 'ipv4_address',
                  'configuration_template', 'router',
                  'check_bgp_session_states', 'comment',)
        help_texts = {
            'name': 'Full name of the Internet Exchange point',
            'ipv6_address': 'IPv6 Address used to peer',
            'ipv4_address': 'IPv4 Address used to peer',
            'configuration_template': 'Template for configuration generation',
            'router': 'Router connected to the Internet Exchange point',
            'check_bgp_session_states': 'If enabled, with a usable router, the state of peering sessions will be updated.',
        }


class InternetExchangeCommunityForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = InternetExchange
        fields = ('communities',)

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            # Get the IX object and remove it from kwargs in order to avoid
            # propagating when calling super
            instance = kwargs.pop('instance')
            # Prepare initial communities
            initial = kwargs.setdefault('initial', {})
            # Add primary key for each community
            initial['communities'] = [
                c.pk for c in instance.communities.all()]

        super(InternetExchangeCommunityForm, self).__init__(*args, **kwargs)

    def save(self):
        instance = forms.ModelForm.save(self)
        instance.communities.clear()

        for community in self.cleaned_data['communities']:
            instance.communities.add(community)


class InternetExchangeFilterForm(BootstrapMixin, forms.Form):
    model = InternetExchange
    q = forms.CharField(required=False, label='Search')
    name = forms.CharField(required=False, label='IX Name')
    ipv6_address = forms.CharField(required=False, label='IPv6 Address')
    ipv4_address = forms.CharField(required=False, label='IPv4 Address')
    configuration_template = FilterChoiceField(
        queryset=ConfigurationTemplate.objects.all(), to_field_name='pk',
        null_label='-- None --')
    router = FilterChoiceField(
        queryset=Router.objects.all(), to_field_name='pk',
        null_label='-- None --')


class PeerRecordFilterForm(BootstrapMixin, forms.Form):
    model = PeerRecord
    q = forms.CharField(required=False, label='Search')
    network__asn = forms.IntegerField(required=False, label='ASN')
    network__name = forms.CharField(required=False, label='AS Name')
    network__irr_as_set = forms.CharField(required=False, label='IRR AS-SET')
    network__info_prefixes6 = forms.IntegerField(required=False,
                                                 label='IPv6 Max Prefixes')
    network__info_prefixes4 = forms.IntegerField(required=False,
                                                 label='IPv4 Max Prefixes')


class PeeringSessionForm(BootstrapMixin, forms.ModelForm):
    comment = CommentField()
    password = PasswordField(required=False, render_value=True)
    enabled = YesNoField(required=False, label='Enabled')

    class Meta:
        model = PeeringSession
        fields = ('autonomous_system', 'internet_exchange',
                  'ip_address', 'password', 'enabled', 'comment',)
        labels = {
            'autonomous_system': 'AS',
            'internet_exchange': 'IX',
            'ip_address': 'IP Address',
            'enabled': 'Enabled',
            'comment': 'Comments',
        }
        help_texts = {
            'ip_address': 'IPv6 or IPv4 address',
            'enabled': 'Should this session be enabled?'
        }


class PeeringSessionFilterForm(BootstrapMixin, forms.Form):
    model = PeeringSession
    q = forms.CharField(required=False, label='Search')
    autonomous_system__asn = forms.IntegerField(required=False, label='ASN')
    autonomous_system__name = forms.CharField(required=False, label='AS Name')
    internet_exchange__name = forms.CharField(required=False, label='IX Name')
    ip_address = forms.CharField(required=False, label='IP Address')
    ip_version = forms.IntegerField(required=False, label='IP Version',
                                    widget=forms.Select(choices=[
                                        (0, '---------'),
                                        (6, 'IPv6'), (4, 'IPv4'),
                                    ]))
    enabled = YesNoField(required=False, label='Enabled')


class PeeringSessionFilterFormForIX(BootstrapMixin, forms.Form):
    model = PeeringSession
    q = forms.CharField(required=False, label='Search')
    autonomous_system__asn = forms.IntegerField(required=False, label='ASN')
    autonomous_system__name = forms.CharField(required=False, label='AS Name')
    ip_address = forms.CharField(required=False, label='IP Address')
    ip_version = forms.IntegerField(required=False, label='IP Version',
                                    widget=forms.Select(choices=[
                                        (0, '---------'),
                                        (6, 'IPv6'), (4, 'IPv4'),
                                    ]))
    enabled = YesNoField(required=False, label='Enabled')


class PeeringSessionFilterFormForAS(BootstrapMixin, forms.Form):
    model = PeeringSession
    q = forms.CharField(required=False, label='Search')
    ip_address = forms.CharField(required=False, label='IP Address')
    ip_version = forms.IntegerField(required=False, label='IP Version',
                                    widget=forms.Select(choices=[
                                        (0, '---------'),
                                        (6, 'IPv6'), (4, 'IPv4'),
                                    ]))
    enabled = YesNoField(required=False, label='Enabled')
    internet_exchange__slug = FilterChoiceField(
        queryset=InternetExchange.objects.all(), to_field_name='slug',
        label='Internet Exchange')


class RouterForm(BootstrapMixin, forms.ModelForm):
    comment = CommentField()

    class Meta:
        model = Router

        fields = ('name', 'hostname', 'platform', 'comment',)
        labels = {
            'comment': 'Comments',
        }
        help_texts = {
            'hostname': 'Router hostname (must be resolvable) or IP address',
        }


class RouterCSVForm(BootstrapMixin, forms.ModelForm):
    platform = CSVChoiceField(choices=PLATFORM_CHOICES, required=False,
                              help_text='The router platform, used to interact with it')

    class Meta:
        model = Router

        fields = ('name', 'hostname', 'platform', 'comment',)
        labels = {
            'comment': 'Comments',
        }
        help_texts = {
            'hostname': 'Router hostname (must be resolvable) or IP address',
        }


class RouterFilterForm(BootstrapMixin, forms.Form):
    model = Router
    q = forms.CharField(required=False, label='Search')
    name = forms.CharField(required=False, label='Router Name')
    hostname = forms.CharField(required=False, label='Router Hostname')
    platform = forms.MultipleChoiceField(choices=PLATFORM_CHOICES,
                                         required=False)
