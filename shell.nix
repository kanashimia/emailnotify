{ pkgs ? import <nixpkgs> {} }:

let
myAppEnv = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    editablePackageSources = {
      emailnotify = ./emailnotify;
    };
    overrides = pkgs.poetry2nix.overrides.withDefaults (self: super: {
      inherit (pkgs.pythonPackages) keyring;
    });
  };
in
pkgs.mkShell {
  buildInputs = [ myAppEnv pkgs.poetry pkgs.libnotify ];
}

