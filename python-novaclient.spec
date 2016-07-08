%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname novaclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:             python-novaclient
Epoch:            1
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Nova
License:          ASL 2.0
URL:              https://bugs.launchpad.net/python-novaclient
Source0:          http://tarballs.openstack.org/python-novaclient/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch

%description
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

%package -n python2-%{sname}
Summary:          Python API and CLI for OpenStack Nova
%{?python_provide:%python_provide python2-novaclient}

BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    python-setuptools

Requires:         python-babel
Requires:         python-iso8601
Requires:         python-keystoneauth1
Requires:         python-oslo-i18n
Requires:         python-oslo-serialization
Requires:         python-oslo-utils
Requires:         python-pbr
Requires:         python-prettytable
Requires:         python-requests
Requires:         python-simplejson
Requires:         python-six
Requires:         python-setuptools

%description -n python2-%{sname}
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Nova
%{?python_provide:%python_provide python3-novaclient}

BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools

Requires:         python3-babel
Requires:         python3-iso8601
Requires:         python3-keystoneauth1
Requires:         python3-oslo-i18n
Requires:         python3-oslo-serialization
Requires:         python3-oslo-utils
Requires:         python3-pbr
Requires:         python3-prettytable
Requires:         python3-requests
Requires:         python3-simplejson
Requires:         python3-six
Requires:         python3-setuptools

%description -n python3-%{sname}
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.
%endif

%package doc
Summary:          Documentation for OpenStack Nova API Client

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

This package contains auto-generated documentation.

%prep
%setup -q -n %{name}-%{upstream_version}

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/nova %{buildroot}%{_bindir}/nova-%{python3_version}
ln -s ./nova-%{python3_version} %{buildroot}%{_bindir}/nova-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/novaclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/nova %{buildroot}%{_bindir}/nova-%{python2_version}
ln -s ./nova-%{python2_version} %{buildroot}%{_bindir}/nova-2

ln -s ./nova-2 %{buildroot}%{_bindir}/nova

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/nova.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/nova

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/novaclient/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html
sphinx-build -b man doc/source man

install -p -D -m 644 man/nova.1 %{buildroot}%{_mandir}/man1/nova.1

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files -n python2-%{sname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/nova.1.gz
%{_bindir}/nova
%{_bindir}/nova-2
%{_bindir}/nova-%{python2_version}


%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/nova.1.gz
%{_bindir}/nova-3
%{_bindir}/nova-%{python3_version}
%endif

%files doc
%doc html
%license LICENSE

%changelog
