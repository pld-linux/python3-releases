#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-releases.spec)

Summary:	Sphinx extension for changelog manipulation
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do operacji na rejestrze zmian
Name:		python-releases
# keep 1.x here for python2 support
Version:	1.6.3
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/releases/
Source0:	https://files.pythonhosted.org/packages/source/r/releases/releases-%{version}.tar.gz
# Source0-md5:	e3334a7ba426f895fb817a6147eefb7c
Patch0:		releases-sphinx1.8.patch
# https://github.com/bitprophet/releases/pull/86.patch (adjusted for 2.1.1)
Patch1:		releases-semantic_version.patch
Patch2:		releases-requires.patch
URL:		https://pypi.org/project/releases/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-Sphinx >= 1.8
BuildRequires:	python-mock >= 1.0.1
BuildRequires:	python-semantic_version
BuildRequires:	python-six >= 1.4.1
BuildRequires:	python-spec >= 0.11.3
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 1.8
BuildRequires:	python3-mock >= 1.0.1
BuildRequires:	python3-semantic_version
BuildRequires:	python3-six >= 1.4.1
BuildRequires:	python3-spec >= 0.11.3
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-sphinx_rtd_theme >= 0.1.5
BuildRequires:	sphinx-pdg-2 >= 1.8
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Releases is a Sphinx extension designed to help you keep a source
control friendly, merge friendly changelog file & turn it into useful,
human readable HTML output.

%description -l pl.UTF-8
Releases to rozszerzenie Sphinksa zaprojektowane, aby pomóc utrzymywać
plik logu zmian przyjazny dla kontroli wersji i łączenia gałęzi oraz
zamieniać go w przydatne, czytelne dla człowieka wyjście HTML.

%package -n python3-releases
Summary:	Sphinx extension for changelog manipulation
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do operacji na rejestrze zmian
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-releases
Releases is a Sphinx extension designed to help you keep a source
control friendly, merge friendly changelog file & turn it into useful,
human readable HTML output.

%description -n python3-releases -l pl.UTF-8
Releases to rozszerzenie Sphinksa zaprojektowane, aby pomóc utrzymywać
plik logu zmian przyjazny dla kontroli wersji i łączenia gałęzi oraz
zamieniać go w przydatne, czytelne dla człowieka wyjście HTML.

%package apidocs
Summary:	API documentation for Python releases module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona releases
Group:		Documentation

%description apidocs
API documentation for Python releases module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona releases.

%prep
%setup -q -n releases-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
spec-2 -w tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
spec-3 -w tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-2 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/releases
%{py_sitescriptdir}/releases-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-releases
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/releases
%{py3_sitescriptdir}/releases-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
