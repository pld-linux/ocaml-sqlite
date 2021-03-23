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
Version:	4.1.3
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/mmottl/sqlite3-ocaml/archive/v%{version}/sqlite3-ocaml-%{version}.tar.gz
# Source0-md5:	1b7c29a831fb517dfa0df399eaea2ceb
URL:		http://mmottl.github.io/sqlite3-ocaml/
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
%requires_eq ocaml

%description devel
This package contains files needed to develop OCaml programs using
ocaml-sqlite3 library.

%prep
%setup -q -n %{module}-ocaml-%{version}

%build
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--docdir=%{_docdir}/%{name} \
	--destdir=$RPM_BUILD_ROOT

%{__make} -j1 all \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{%{module},stublibs}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	OCAMLFIND_DOCDIR=$RPM_BUILD_ROOT%{_docdir}/%{name}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
ln -sr $RPM_BUILD_ROOT%{_libdir}/ocaml/{%{module},site-lib/%{module}}/META

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc CHANGES.txt README.md TODO.md src/%{module}.mli test
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/sqlite3/META
%{_libdir}/ocaml/sqlite3/sqlite3.annot
%{_libdir}/ocaml/%{module}/*.cm[xi]
%{_libdir}/ocaml/%{module}/*.cma
%{_libdir}/ocaml/%{module}/sqlite3.cmt
%{_libdir}/ocaml/%{module}/sqlite3.cmti
%{_libdir}/ocaml/%{module}/sqlite3.mli
%{_libdir}/ocaml/%{module}/libsqlite3_stubs.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.cmx[as]
%{_libdir}/ocaml/%{module}/sqlite3.a
%endif
%{_libdir}/ocaml/site-lib/%{module}
%{_libdir}/ocaml/stublibs/dllsqlite3_stubs.so.owner
