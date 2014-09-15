
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Name:		reaper
Version:	1.0
Release:	1%{?dist}
Summary:	Resource controller

License:	Apache
URL:		http://github.com/lviana/reaper
Source0:	reaper-%{version}.tar.bz2

BuildRequires:	python, python-devel, python-setuptools
Requires:	python, libcgroup, PyYAML

%description
Reaper is a resource controller for shared hosting environments, it
supports both native implementations of application servers or
Cpanel based shared hosting infrastructure.
It is easy to be extended or adapted to run on other platforms.

%prep
%setup -q -n reaper


%build
%{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT


%files
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/reaper.cfg
%attr(0755,root,root) %{_bindir}/reaperd
%defattr(0644,root,root,-)
%{python_sitelib}/reaper-0.1.0-py2.6.egg-info/PKG-INFO
%{python_sitelib}/reaper-0.1.0-py2.6.egg-info/SOURCES.txt
%{python_sitelib}/reaper-0.1.0-py2.6.egg-info/dependency_links.txt
%{python_sitelib}/reaper-0.1.0-py2.6.egg-info/top_level.txt
%{python_sitelib}/reaper/cgroups.py
%{python_sitelib}/reaper/cgroups.py*
%{python_sitelib}/reaper/collectors.py
%{python_sitelib}/reaper/collectors.py*


%changelog
* Tue Sep  9 2014 Luiz Viana <lviana@include.io> - 1.0-1
- Initial release
