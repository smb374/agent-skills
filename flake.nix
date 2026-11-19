{
  description = "Personal agent skills";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      perSystem =
        { pkgs, ... }:
        {
          devShells.default = pkgs.mkShell {
            packages = [
              (pkgs.python3.withPackages (ps: [ ps.pyyaml ]))
              pkgs.just
              pkgs.nodejs
              pkgs.ruff
              pkgs.nixfmt
              pkgs.shellcheck
            ];
          };
        };
    };
}
