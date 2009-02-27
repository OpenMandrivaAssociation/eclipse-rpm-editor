%define gcj_support         0
%define eclipse_base        %{_datadir}/eclipse
%define eclipse_base        %{_libdir}/eclipse
%define install_loc         %{_datadir}/eclipse/dropins
%define svn_rev             18654
%define debug_package %{nil}

Name:           eclipse-rpm-editor
Version:        0.4.2
Release:        %mkrel 0.1.0
Epoch:          0
Summary:        RPM Specfile editor for Eclipse
Group:          Development/Java
License:        EPL
URL:            http://wiki.eclipse.org/index.php/Linux_Distributions_Project
# This tarball was made using the included script, like so:
#   sh ./fetch-specfile-editor.sh %{svn_rev}
Source0:        specfile-editor-fetched-src-%{version}.tar.bz2
Source1:        fetch-specfile-editor.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif
%if ! %{gcj_support}
BuildArch: noarch
%endif
BuildRequires: java-rpmbuild
BuildRequires: zip
BuildRequires: eclipse-pde >= 1:3.3.0
BuildRequires: eclipse-changelog >= 2.5.1
Requires: eclipse-platform >= 3.3.1
Requires: eclipse-changelog >= 2.5.1
Requires: rpmlint >= 0.81
Requires: rpmdevtools

# These plugins are really noarch but they the changelog plugin need cdt which
# we only build on these architectures.
%if %{gcj_support}
ExclusiveArch: %{ix86} x86_64 ppc ia64
%else
ExclusiveArch: %{ix86} x86_64 ppc ia64 noarch
%endif

%description
The Eclipse Specfile Editor package contains Eclipse plugins that are
useful for maintenance of RPM specfiles within the Eclipse IDE.

%prep
%setup -q -n specfile-editor-fetched-src-%{version}

%build
# See comments in the script to understand this.
%{eclipse_base}/buildscripts/pdebuild -d changelog -f org.eclipse.linuxtools.rpm.ui.editor \
  -a "-DjavacTarget=1.6 -DjavacSource=1.6"

%install
rm -rf %{buildroot}
installDir=%{buildroot}%{install_loc}/rpm-editor
install -d -m 755 $installDir
unzip -q -d $installDir \
 build/rpmBuild/org.eclipse.linuxtools.rpm.ui.editor.zip

%{gcj_compile}

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%doc org.eclipse.linuxtools.rpm.ui.editor-feature/*.html
%{install_loc}/rpm-editor
%{gcj_files}
