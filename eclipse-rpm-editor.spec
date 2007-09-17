%define gcj_support         1
%define eclipse_base        %{_datadir}/eclipse
%define svn_rev             2610

Name:           eclipse-rpm-editor
Version:        0.1.0
Release:        %mkrel 0.7.1
Epoch:          0
Summary:        RPM Specfile editor for Eclipse
Group:          Development/Java
License:        EPL
URL:            http://wiki.eclipse.org/index.php/Linux_Distributions_Project
# This tarball was made using the included script, like so:
#   sh ./fetch-specfile-editor.sh %{svn_rev}
Source0:        specfile-editor-fetched-src-%{svn_rev}.tar.bz2
Source1:        fetch-specfile-editor.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%else
BuildRequires:    java-devel >= 1.5.0
%endif
%if ! %{gcj_support}
BuildArch: noarch
%endif
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
ExclusiveArch: %{ix86} x86_64 ppc ia64
%endif

%description
The Eclipse Specfile Editor package contains Eclipse plugins that are
useful for maintenance of RPM specfiles within the Eclipse IDE.

%prep
%setup -q -n specfile-editor-fetched-src-%{svn_rev}

%build
# See comments in the script to understand this.
/bin/sh -x %{_datadir}/eclipse/buildscripts/copy-platform SDK %{eclipse_base} changelog
SDK=$(cd SDK > /dev/null && pwd)

# Eclipse may try to write to the home directory.
mkdir home
homedir=$(cd home > /dev/null && pwd)

%{java} -cp $SDK/startup.jar \
     -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration \
     org.eclipse.core.launcher.Main \
     -application org.eclipse.ant.core.antRunner \
     -Dtype=feature \
     -Did=org.eclipse.linuxtools.rpm.ui.editor \
     -DbaseLocation=$SDK \
     -DsourceDirectory=$(pwd) \
     -DbuildDirectory=$(pwd)/build \
     -Dbuilder=%{eclipse_base}/plugins/org.eclipse.pde.build/templates/package-build \
     -f %{eclipse_base}/plugins/org.eclipse.pde.build/scripts/build.xml \
     -vmargs -Duser.home=$homedir \

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{eclipse_base}
unzip -q -d %{buildroot}%{eclipse_base}/.. \
 build/rpmBuild/org.eclipse.linuxtools.rpm.ui.editor.zip

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(-,root,root,-)
%{eclipse_base}/plugins/org.eclipse.linuxtools.rpm.ui.editor_*.jar
%{eclipse_base}/plugins/org.eclipse.linuxtools.rpm.rpmlint_*.jar
%dir %{eclipse_base}/features/org.eclipse.linuxtools.rpm.ui.editor_*/
%doc %{eclipse_base}/features/org.eclipse.linuxtools.rpm.ui.editor_*/*.html
%{eclipse_base}/features/org.eclipse.linuxtools.rpm.ui.editor_*/*.xml
%{eclipse_base}/features/org.eclipse.linuxtools.rpm.ui.editor_*/*.properties
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/org.eclipse.linuxtools.rpm.*
%endif