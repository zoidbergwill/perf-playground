# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/artful64"

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys D4284CDD
    echo "deb https://repo.iovisor.org/apt/xenial xenial main" | tee /etc/apt/sources.list.d/iovisor.list
    apt-get update
    apt-get install auditd bcc-tools libbcc-examples linux-headers-$(uname -r)
  SHELL
end
