{
  description = "Auto Analytics Flake (pandas + ydata-profiling)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};
        python-env = pkgs.python3.withPackages (ps:
          with ps; [
            pandas
            ydata-profiling
          ]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [python-env];
          shellHook = ''
            echo "Ready! Run your Python analytics script."
          '';
        };
      }
    );
}
