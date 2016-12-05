#!/usr/bin/env bash
set -ex

ansible-playbook provision-pi-playbook.yml -i hosts --vault-password-file ~/.vault_pass.txt
