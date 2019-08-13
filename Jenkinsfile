def install_tar = "quipucords_install.tar"
def install_targzfile = "${install_tar}.gz"
def install_sh_path = "install/quipucords-installer"

node('f28-os') {
    stage('Build Install tar.gz') {
        checkout scm
        sh "sed -i s/BUILD_VERSION_PLACEHOLDER/${BUILD_VERSION}/g ${install_sh_path}"
        sh "sudo tar -cvf $install_tar install/*"
        sh "sudo chmod 755 $install_tar"
        sh "sudo gzip -f --best $install_tar"
        sh "sudo chmod 755 $install_targzfile"

        archiveArtifacts install_targzfile
    }
}
