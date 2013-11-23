# TODO
# - tests. W: Tests are turned off, consider enabling with 'ocaml setup.ml -configure --enable-tests'
#
# Conditional build:
%bcond_with	opt		# build opt

Summary:	sqlite3 binding for OCaml
Name:		ocaml-sqlite
Version:	2.0.4
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://bitbucket.org/mmottl/sqlite3-ocaml/downloads/sqlite3-ocaml-%{version}.tar.gz
# Source0-md5:	ae90c81f24322afad47678ffdc6c2a64
URL:		https://bitbucket.org/mmottl/sqlite3-ocaml
BuildRequires:	ocaml-findlib-devel
BuildRequires:	ocaml-camlp4
BuildRequires:	sqlite3-devel
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SQLite 3 database library wrapper for OCaml.

%package devel
Summary:	sqlite3 binding for OCaml - development part
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
ocaml-sqlite3 library.

%prep
%setup -q -n sqlite3-ocaml-%{version}

%build
./configure \
	--libdir=%{_libdir}

%{__make} -j1 all %{?with_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{sqlite3,stublibs}
cp -p _build/lib/*.cm[ixa]* _build/lib/*.a $RPM_BUILD_ROOT%{_libdir}/ocaml/sqlite3
install -p _build/lib/dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/sqlite3
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/sqlite3/META <<EOF
requires = ""
version = "%{version}"
description="Ocaml bindings to Sqlite 3"
directory = "+sqlite3"
archive(byte) = "sqlite3.cma"
archive(native) = "sqlite3.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc CHANGES.txt README.md TODO.md lib/sqlite3.mli test
%dir %{_libdir}/ocaml/sqlite3
%{_libdir}/ocaml/sqlite3/*.cm[ixa]*
%{_libdir}/ocaml/sqlite3/*.a
%{_libdir}/ocaml/site-lib/sqlite3
