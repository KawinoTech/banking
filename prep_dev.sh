#!/usr/bin/env bash
git config --global user.name "Okoth Kawino"
git config --global user.email "techkawino@gmail.com"
touch .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".vscode/" >> .gitignore
git config --global color.ui auto
git config --global alias.cm commit
sudo apt-get update
sudo apt install gpg -y
git config --global gpg.program $(which gpg)
export GPG_TTY=$(tty)
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
sudo gpg --full-generate-key
key=$(gpg --list-secret-keys --keyid-format=long | grep "sec" | cut -d "/" -f 2 | cut -d " " -f 1)
echo "Key ID = $key"
echo "Telling Git to use your GPG key to sign commits..."
git config --global user.signingkey $key

git config --global commit.gpgsign true
gpg --armor --export techkawino@gmail.com
