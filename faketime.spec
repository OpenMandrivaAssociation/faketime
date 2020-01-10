%define major 1
%define libname %mklibname %{name} %{major}
%define libnamemt %mklibname %{name}MT %{major}

Summary:	Report faked system time to programs
Name:		faketime
Version:	0.9.8
Release:	1
License:	GPLv2+
Group:		Development/Other
Url:		http://www.code-wizards.com/projects/libfaketime/
Source0:	https://github.com/wolfcw/libfaketime/archive/v%{version}.tar.gz
Patch1:		faketime-0.9.6-comparison-nonnull-parameter-a-true.patch
Requires:	%{libname} = %{EVRD}
Requires:	%{libnamemt} = %{EVRD}

%description
libfaketime intercepts various system calls which programs use to
retrieve the current date and time. It can then report faked dates and
times (as specified by you, the user) to these programs. This means you
can modify the system time a program sees without having to change the
time system-wide.

%files
%doc README NEWS
%{_bindir}/faketime
%{_mandir}/man1/faketime.1*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Faketime shared library
Group:		System/Libraries
Conflicts:	%{name} < 0.9.5

%description -n %{libname}
Faketime shared library.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libnamemt}
Summary:	Faketime shared library
Group:		System/Libraries
Conflicts:	%{name} < 0.9.5

%description -n %{libnamemt}
Faketime shared library.

%files -n %{libnamemt}
%{_libdir}/lib%{name}MT.so.%{major}*

#----------------------------------------------------------------------------

%prep
%setup -q -n libfaketime-%{version}
%autopatch -p1

# work around from upstream for autodetecting glibc version bug on i686
sed -i -e 's/__asm__(".symver timer_gettime_22/\/\/__asm__(".symver timer_gettime_22/' src/libfaketime.c
sed -i -e 's/__asm__(".symver timer_settime_22/\/\/__asm__(".symver timer_settime_22/' src/libfaketime.c

#https://github.com/wolfcw/libfaketime/issues/75
sed -i -e 's!-Werror!!'g src/Makefile

%build
export CC=gcc
%global optflags %{optflags} -Wno-error -Wno-pointer-bool-conversion
%setup_compile_flags
%make PREFIX=%{_prefix} LIBDIRNAME=/%{_lib}

%install
%makeinstall_std PREFIX=%{_prefix} LIBDIRNAME=/%{_lib}

chmod 0755 %{buildroot}%{_libdir}/lib%{name}*.so.%{major}*
