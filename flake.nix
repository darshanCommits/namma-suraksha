{
  description = "";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };

  outputs = {
    self,
    nixpkgs,
    ...
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        python3
        ruff
        python311Packages.python-lsp-server
        python311Packages.pylsp-rope
      ];

      shellHook = ''
        export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
          pkgs.stdenv.cc.cc.lib
          pkgs.libz
        ]}:$LD_LIBRARY_PATH
        export PYTHONPATH=$PYTHONPATH:$(pwd)
        export DJANGO_SETTINGS_MODULE=src.settings

        if [ -d "./venv" ]; then
          source ./venv/bin/activate
        else
          echo "No venv found. You can create one with 'python -m venv venv'"
        fi
      '';
    };
  };
}
