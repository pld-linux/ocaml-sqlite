# TODO
# - tests. W: Tests are turned off, consider enabling with 'ocaml setup.ml -configure --enable-tests'
#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	sqlite3
Summary:	sqlite3 binding for OCaml
Name:		ocaml-sqlite
Version:	2.0.4
Release:	3
License:	BSD
Group:		Libraries
Source0:	https://bitbucket.org/mmottl/sqlite3-ocaml/downloads/sqlite3-ocaml-%{version}.tar.gz
# Source0-md5:	ae90c81f24322afad47678ffdc6c2a64
URL:		https://bitbucket.org/mmottl/sqlite3-ocaml
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-findlib-devel
BuildRequires:	sqlite3-devel
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
%setup -q -n %{module}-ocaml-%{version}

%build
./configure \
	--libdir=%{_libdir}

%{__make} -j1 all %{?with_ocaml_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{%{module},stublibs}
cp -p _build/lib/*.cm[ixa]* _build/lib/*.a $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}
install -p _build/lib/dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META <<EOF
requires = ""
version = "%{version}"
description="Ocaml bindings to Sqlite3"
directory = "+%{module}"
archive(byte) = "%{module}.cma"
archive(native) = "%{module}.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc CHANGES.txt README.md TODO.md lib/%{module}.mli test
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/*.cm[xi]
%{_libdir}/ocaml/%{module}/*.cma
%{_libdir}/ocaml/%{module}/libsqlite3_stubs.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.cmx[as]
%{_libdir}/ocaml/%{module}/sqlite3.a
%endif
%{_libdir}/ocaml/site-lib/%{module}
