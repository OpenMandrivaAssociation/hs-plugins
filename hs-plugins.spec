%define hs_package hs-plugins

Summary:	A library for loading code written in Haskell into an application at runtime
Name:		%{hs_package}
Version: 	0.9.11
Release: 	%mkrel 0.20051120.2
Source0: 	ftp://ftp.cse.unsw.edu.au/pub/users/dons/hs-plugins/%{hs_package}.tar.gz
License: 	LGPL
Group:		Development/Other
Url: 		http://www.cse.unsw.edu.au/~dons/hs-plugins/
Buildrequires:	ghc
Buildrequires:	haskell-src-exts
Requires:	ghc

%description
hs-plugins is a library for loading code written in Haskell into an application
at runtime, in the form of plugins. It also provides a mechanism for
(re-)compiling Haskell source at runtime. Thirdly, a combination of runtime
compilation and dynamic loading provides a set of eval functions- a form of
runtime metaprogramming. Values exported by Haskell plugins are transparently
available to Haskell host applications, and bindings exist to use Haskell
plugins from at least C and Objective C programs.

%prep
%setup -q -n %{hs_package}
# replace the Setup.hs file by a working one
cat > Setup.hs << EOF
import Distribution.Simple
main = defaultMainWithHooks defaultUserHooks
EOF
chmod +x configure

%build
runhaskell Setup configure --ghc -v --prefix=%{_prefix}
runhaskell Setup build -v

# generate register and unregister scripts
runhaskell Setup register --gen-script
runhaskell Setup unregister --gen-script

%install
rm -rf $RPM_BUILD_ROOT

runhaskell Setup copy  --copy-prefix=$RPM_BUILD_ROOT/%{_prefix}

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}
cp register.sh $RPM_BUILD_ROOT/%{_datadir}/%{name}
cp unregister.sh $RPM_BUILD_ROOT/%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*
%{_datadir}/*
#%doc Abrechnung.lhs dot.lhs Tests.lhs

%post -p %{_datadir}/%{name}/register.sh

%preun -p %{_datadir}/%{name}/unregister.sh

