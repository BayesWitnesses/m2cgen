#!/bin/bash

set -e

# Install .NET Core SDK.
if [[ $LANG == *"c_sharp"* ]] || [[ $LANG == *"f_sharp"* ]] || [[ $LANG == *"visual_basic"* ]]; then
  wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb
  sudo dpkg -i packages-microsoft-prod.deb
  sudo apt-get update
  sudo apt-get install --no-install-recommends -y dotnet-sdk-3.1
fi

# Install PowerShell Core.
if [[ $LANG == *"powershell"* ]]; then
  wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb
  sudo dpkg -i packages-microsoft-prod.deb
  sudo apt-get update
  sudo apt-get install --no-install-recommends -y powershell
fi

# Install R.
if [[ $LANG == *"r_lang"* ]]; then
  sudo apt-get update
  sudo apt-get install --no-install-recommends -y r-base
fi

# Install PHP.
if [[ $LANG == *"php"* ]]; then
  sudo apt-get update
  sudo apt-get install --no-install-recommends -y php
fi

# Install Dart. (https://dart.dev/get-dart)
if [[ $LANG == *"dart"* ]]; then
  sudo sh -c 'wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -'
  sudo sh -c 'wget -qO- https://storage.googleapis.com/download.dartlang.org/linux/debian/dart_stable.list > /etc/apt/sources.list.d/dart_stable.list'
  sudo apt-get update
  sudo apt-get install --no-install-recommends -y dart
fi

# Install Haskell.
if [[ $LANG == *"haskell"* ]]; then
  sudo apt-get update
  sudo apt-get install --no-install-recommends -y haskell-platform
fi

# Install Ruby.
if [[ $LANG == *"ruby"* ]]; then
  sudo apt-get update
  sudo apt-get install --no-install-recommends -y ruby-full
fi
