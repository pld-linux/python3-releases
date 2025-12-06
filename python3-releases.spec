#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Sphinx extension for changelog manipulation
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do operacji na rejestrze zmian
Name:		python3-releases
Version:	2.1.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/releases/
Source0:	https://files.pythonhosted.org/packages/source/r/releases/releases-%{version}.tar.gz
# Source0-md5:	9e9309dbe0f7acdd3e3d69e7e29a3730
# https://github.com/bitprophet/releases/pull/86.patch (adjusted for 2.1.1)
Patch0:		releases-semantic_version.patch
Patch1:		releases-requires.patch
URL:		https://pypi.org/project/releases/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 4
BuildRequires:	python3-icecream >= 2.1.3
BuildRequires:	python3-pytest >= 4.6.9
BuildRequires:	python3-pytest-relaxed >= 2
BuildRequires:	python3-semantic_version
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme >= 0.1.5
BuildRequires:	sphinx-pdg-3 >= 4
%endif
Requires:	python3-modules >= 1:3.6
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

%build
%py3_build

%if %{with tests}
# disabled test fails with Sphinx 7.3+
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_relaxed.plugin \
%{__python3} -m pytest tests -k 'not unused_kwargs_become_releases_config_options'
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/releases
%{py3_sitescriptdir}/releases-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
