%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             python-novaclient
Epoch:            1
Version:          3.3.1
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Nova

Group:            Development/Languages
License:          ASL 2.0
URL:              http://pypi.python.org/pypi/%{name}
Source0:          http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python-d2to1
BuildRequires:    python-keystoneclient
BuildRequires:    python-netifaces
BuildRequires:    python-pbr
BuildRequires:    python-setuptools

Requires:         python-argparse
Requires:         python-babel
Requires:         python-iso8601
Requires:         python-keyring
Requires:         python-keystoneauth1
Requires:         python-keystoneclient
Requires:         python-netifaces
Requires:         python-oslo-i18n
Requires:         python-oslo-serialization
Requires:         python-oslo-utils
Requires:         python-pbr
Requires:         python-prettytable
Requires:         python-requests
Requires:         python-simplejson
Requires:         python-six
Requires:         python-setuptools

%description
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

%package doc
Summary:          Documentation for OpenStack Nova API Client
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

This package contains auto-generated documentation.

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove bundled egg-info
rm -rf python_novaclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/nova.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/nova

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/novaclient/tests
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html
sphinx-build -b man doc/source man

install -p -D -m 644 man/nova.1 %{buildroot}%{_mandir}/man1/nova.1

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc README.rst
%doc LICENSE
%{_bindir}/nova
%{python2_sitelib}/novaclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/nova.1.gz

%files doc
%doc html

%changelog
* Fri Apr 15 2016 Haikel Guemar <hguemar@fedoraproject.org> 1:3.3.1-1
- Update to 3.3.1

* Wed Mar 23 2016 Haikel Guemar <hguemar@fedoraproject.org> 1:3.3.0-
- Update to 3.3.0

