#!/bin/bash

set -e

# Install .NET Core SDK.
if [[ $LANG == *"c_sharp"* ]] || [[ $LANG == *"visual_basic"* ]]; then
  wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb
  sudo dpkg -i packages-microsoft-prod.deb
  sudo apt-get update
  sudo apt-get install --no-install-recommends -y dotnet-sdk-3.0
fi

# Install PowerShell Core.
if [[ $LANG == *"powershell"* ]]; then
  wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb
  sudo dpkg -i packages-microsoft-prod.deb
  sudo apt-get update
  sudo apt-get install --no-install-recommends -y powershell
fi
