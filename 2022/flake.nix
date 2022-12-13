{
  description = "Advent of code 2022";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        advent = pkgs.stdenv.mkDerivation {
          name = "advent-2022";
          src = self;
          buildInputs = with pkgs; [
            gdb
            rr
            flamegraph
            cmake
            gtest
            clang_14
            perf-tools
            linuxPackages_latest.perf
          ];
          hardeningDisable = [ "fortify" ];
        };

      in { packages.default = advent; });
}
