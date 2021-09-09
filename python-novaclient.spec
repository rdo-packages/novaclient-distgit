%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x4c29ff0e437f3351fd82bdf47c5a3bc787dc7035
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname novaclient
%global with_doc 1

%global common_desc \
This is a client for the OpenStack Nova API. There's a Python API (the \
novaclient module), and a command-line script (nova). Each implements 100% of \
the OpenStack Nova API.

Name:             python-novaclient
Epoch:            1
Version:          17.6.0
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Nova
License:          ASL 2.0
URL:              https://launchpad.net/%{name}
Source0:          https://pypi.io/packages/source/p/%{name}/%{name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Nova
%{?python_provide:%python_provide python3-novaclient}
Obsoletes: python2-%{sname} < %{version}-%{release}

BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools

Requires:         python3-iso8601 >= 0.1.11
Requires:         python3-keystoneauth1 >= 3.5.0
Requires:         python3-oslo-i18n >= 3.15.3
Requires:         python3-oslo-serialization >= 2.18.0
Requires:         python3-oslo-utils >= 3.33.0
Requires:         python3-pbr >= 2.0.0
Requires:         python3-prettytable >= 0.7.2
Requires:         python3-stevedore >= 2.0.1

%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Nova API Client

BuildRequires:    python3-sphinx
BuildRequires:    python3-sphinxcontrib-apidoc
BuildRequires:    python3-openstackdocstheme
BuildRequires:    python3-oslo-utils
BuildRequires:    python3-keystoneauth1
BuildRequires:    python3-oslo-serialization
BuildRequires:    python3-prettytable

%description      doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

# Let RPM handle the requirements
%py_req_cleanup

%build
%{py3_build}

%install
%{py3_install}
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s nova %{buildroot}%{_bindir}/nova-3

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/nova.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/nova

# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/novaclient/tests

%if 0%{?with_doc}
sphinx-build -b html doc/source doc/build/html
sphinx-build -b man doc/source doc/build/man

install -p -D -m 644 doc/build/man/nova.1 %{buildroot}%{_mandir}/man1/nova.1

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo doc/build/html/.htaccess
%endif

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%if 0%{?with_doc}
%{_mandir}/man1/nova.1.gz
%endif
%{_bindir}/nova
%{_bindir}/nova-3

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Thu Sep 09 2021 RDO <dev@lists.rdoproject.org> 1:17.6.0-1
- Update to 17.6.0

