%define eclipse_base        %{_libdir}/eclipse
%define install_loc         %{_datadir}/eclipse/dropins
%define qualifier           201007201624

Name:           eclipse-rpm-editor
Version:        0.6.0
Release:        2
Summary:        RPM Specfile editor for Eclipse
Group:          Development/Java
License:        EPL
URL:            http://www.eclipse.org/linuxtools/
# This tarball was made using the included script, like so:
#   sh ./fetch-specfile-editor.sh R0_6_0 0.6.0
Source0:        specfile-editor-fetched-src-%{version}.tar.bz2
Source1:        fetch-specfile-editor.sh
Patch0:         fix_bz319742_backport.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-devel >= 1.5.0
BuildRequires: eclipse-pde >= 0:3.3.0
BuildRequires: eclipse-changelog >= 2.5.1
Requires: eclipse-platform >= 3.3.1
Requires: eclipse-changelog >= 2.5.1
Requires: rpmlint >= 0.81
Requires: rpmdevtools

# These plugins are really noarch but the changelog plugin need cdt which
# we only build on these architectures.
ExclusiveArch: %{ix86} x86_64 ppc ia64
%define debug_package %{nil}

%description
The Eclipse Specfile Editor package contains Eclipse plugins that are
useful for maintenance of RPM specfiles within the Eclipse IDE.

%prep
%setup -q -n specfile-editor-fetched-src-%{version}
%patch0
pushd org.eclipse.linuxtools.rpm.ui.editor
popd

%build
%{eclipse_base}/buildscripts/pdebuild -a "-DforceContextQualifier=%{qualifier} -DjavacSource=1.5 -DjavacTarget=1.5" \
 -f  org.eclipse.linuxtools.rpm
%{eclipse_base}/buildscripts/pdebuild -a "-DforceContextQualifier=%{qualifier} -DjavacSource=1.5 -DjavacTarget=1.5" \
 -f  org.eclipse.linuxtools.rpm.ui.editor -d changelog ;

%install
rm -rf %{buildroot}
installDir=%{buildroot}%{install_loc}/rpm-editor
install -d -m 755 $installDir
unzip -q -d $installDir \
 build/rpmBuild/org.eclipse.linuxtools.rpm.ui.editor.zip
unzip -q -d $installDir \
 build/rpmBuild/org.eclipse.linuxtools.rpm.zip

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc org.eclipse.linuxtools.rpm.ui.editor-feature/*.html
%{install_loc}/rpm-editor

