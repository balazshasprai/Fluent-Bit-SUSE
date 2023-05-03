#
# spec file for package fluent-bit
#

%define _dest_dir %{_buildrootdir}/destdir

Name:           fluent-bit
Version:        2.0.11
Release:        54
Summary:        Fast data collector for Linux
License:        Apache-2.0
Group:          System/Daemons
Vendor:         Calyptia Inc.
URL:            https://fluentbit.io/
Source0:        fluent-bit-%{version}.tar.gz
Source1:        fluent-bit.service
BuildRequires:  git
BuildRequires:  libyaml-devel
BuildRequires:  libopenssl-devel
BuildRequires:  libedit-devel
BuildRequires:  systemd-devel
BuildRequires:  postgresql-devel
# BuildRequires:  msgpack-devel # TODO unresolvable in SLES builder on OBS?
# BuildRequires:  valgrind-devel # TODO unresolvable in SLES builder on OBS?
BuildRequires:  gcc-c++
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  cmake

%description
Fluent Bit is a high performance and multi platform Log Forwarder.

%prep
%setup -q -n fluent-bit-%{version}


%build
##
## build ####################################################
##
cd build
cmake ../\
    -DCMAKE_BUILD_TYPE=RelWithDebInfo\
    -DFLB_ALL=On\
    -DFLB_TESTS_RUNTIME=On\
    -DFLB_RELEASE=On

#
# - build fluent-bit
#
%make_build

%install
##
## install ##################################################
##
#
cd build
mkdir %{_dest_dir}
make install DESTDIR="%{_dest_dir}"
#
install -d -m755 %{buildroot}%{_bindir}/

install -d -m755 %{buildroot}/etc/fluent-bit

install -d -m755 %{buildroot}/usr/lib/systemd/system
install -d -m755 %{buildroot}/lib64/fluent-bit

install -c -m644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service

install -D -m 0755 %{_dest_dir}/usr/local/bin/%{name} %{buildroot}%{_bindir}/%{name}
install -D -m 0644 %{_dest_dir}/usr/local/etc/fluent-bit/fluent-bit.conf %{buildroot}/etc/fluent-bit/fluent-bit.conf
install -D -m 0644 %{_dest_dir}/usr/local/etc/fluent-bit/parsers.conf %{buildroot}/etc/fluent-bit/parsers.conf
install -D -m 0644 %{_dest_dir}/usr/local/etc/fluent-bit/plugins.conf %{buildroot}/etc/fluent-bit/plugins.conf
install -D -m 0755 %{_dest_dir}/usr/local/lib64/fluent-bit/libfluent-bit.so %{buildroot}/lib64/fluent-bit/libfluent-bit.so

install -d -m755 %{buildroot}%{_sbindir}/
pushd %{buildroot}%{_sbindir}
ln -s service rc%{name}
popd


%pre
%{service_add_pre %{name}.service}

%post
##
## post install #############################################
##
/sbin/ldconfig
%{service_add_post %{name}.service}

%preun
##
## pre uninstall ############################################
##
%{service_del_preun %{name}.service}

%postun
##
## post uninstall ###########################################
##
#
# update linker caches
#
/sbin/ldconfig
%{service_del_postun %{name}.service}

%files
##
## file list ################################################
##
%defattr(-,root,root,-)
"/usr/lib/systemd/system/fluent-bit.service"
"/usr/bin/fluent-bit"
"/usr/sbin/rcfluent-bit"
"/lib64/fluent-bit/libfluent-bit.so"
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/parsers.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins.conf
%dir "/etc/fluent-bit"
%dir "/usr/lib/systemd"
%dir "/usr/lib/systemd/system"
%dir "/lib64/fluent-bit"

%changelog

* Wed May 3 2023 Balázs Hasprai <balazs.hasprai@hbalazs.com> - 2.0.11-54
- Fix install step, create /usr/sbin dir

* Wed May 3 2023 Balázs Hasprai <balazs.hasprai@hbalazs.com> - 2.0.11-54
- Fix rclink "installed but unpackaged files"

* Wed May 3 2023 Balázs Hasprai <balazs.hasprai@hbalazs.com> - 2.0.11-52
- Add rclink in spec's install steps

* Wed May 3 2023 Balázs Hasprai <balazs.hasprai@hbalazs.com> - 2.0.11-51
- Touch up spec file, remove commented license macro, fix /lib->/usr/lib dirs