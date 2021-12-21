# TODO
# - tests. W: Tests are turned off, consider enabling with 'ocaml setup.ml -configure --enable-tests'
#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%if %{without ocaml_opt}
%define		_enable_debug_packages	0
%endif

%define		module	sqlite3
Summary:	SQLite 3 binding for OCaml
Summary(pl.UTF-8):	Wiązanie SQLite 3 dla OCamla
Name:		ocaml-sqlite
Version:	4.4.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/mmottl/sqlite3-ocaml/releases
Source0:	https://github.com/mmottl/sqlite3-ocaml/releases/download/%{version}/sqlite3-%{version}.tbz
# Source0-md5:	93763885a3606252aa8004f7662dd161
URL:		http://mmottl.github.io/sqlite3-ocaml/
BuildRequires:	ocaml >= 1:4.05
BuildRequires:	ocaml-dune >= 1.4.0
BuildRequires:	ocaml-findlib-devel
BuildRequires:	ocaml-stdio-devel
BuildRequires:	sqlite3-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SQLite 3 database library wrapper for OCaml.

%description -l pl.UTF-8
Obudowanie biblioteki baz danych SQLite 3 dla OCamla.

%package devel
Summary:	SQLite 3 binding for OCaml - development part
Summary(pl.UTF-8):	Wiązanie SQLite 3 dla OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
ocaml-sqlite3 library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki ocaml-sqlite3.

%prep
%setup -q -n sqlite3-%{version}

%build
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/%{module}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.md TODO.md pre-v4.2.0-CHANGES.txt
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/META
%{_libdir}/ocaml/%{module}/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/%{module}/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllsqlite3_stubs.so
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/%{module}/libsqlite3_stubs.a
%{_libdir}/ocaml/%{module}/*.cmi
%{_libdir}/ocaml/%{module}/*.cmt
%{_libdir}/ocaml/%{module}/*.cmti
%{_libdir}/ocaml/%{module}/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/sqlite3.a
%{_libdir}/ocaml/%{module}/*.cmx
%{_libdir}/ocaml/%{module}/*.cmxa
%endif
%{_libdir}/ocaml/%{module}/dune-package
%{_libdir}/ocaml/%{module}/opam
