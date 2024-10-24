{ pkgs, lib, config, inputs, ... }:
{
  packages = with pkgs; [ more ];

  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = ./requirements.txt;
    };
  };

  languages.javascript = {
    enable = true;
    npm.enable = true;
  };
}