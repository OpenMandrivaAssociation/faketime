Name:		faketime
Version:	0.9.1
Release:	1
Summary:	Run programs with a faked system time
License:	GPLv2
Group:		Development/Other
URL:		http://www.code-wizards.com/projects/libfaketime/

Source0:	http://www.code-wizards.com/projects/libfaketime/libfaketime-%{version}.tar.gz

%description
The Fake Time Preload Library (FTPL or libfaketime) intercepts various system
calls which programs use to retrieve the current date and time. It can then
report faked dates and times (as specified by you, the user) to these programs.
This means you can modify the system time a program sees without having to
change the time system-wide.

%prep
%setup -q -n libfaketime-%{version}

%build
%make
gzip -f man/faketime.1
# Fix path to the installed faketime
sed -i "s|FTPL_PATH=/usr/lib/faketime|FTPL_PATH=%{_libdir}|" src/faketime

%install
install -Dm0644 src/libfaketime.so.1 %{buildroot}%{_libdir}/libfaketime.so.1
install -Dm0644 src/libfaketimeMT.so.1 %{buildroot}%{_libdir}/libfaketimeMT.so.1
install -Dm0755 src/faketime %{buildroot}%{_bindir}/faketime
install -Dm0644 man/faketime.1.gz %{buildroot}%{_mandir}/man1/faketime.1.gz

%files
%_bindir/*
%_libdir/*.so.*
%_mandir/man?/*
