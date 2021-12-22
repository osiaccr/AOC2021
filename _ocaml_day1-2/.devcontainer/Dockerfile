FROM ocaml/opam2:4.08

USER root

RUN git -C /home/opam/opam-repository pull origin master && opam update

RUN opam install \
  base core_kernel \
  ounit qcheck dune \
  ocamlformat merlin core

# Add opam binaries to PATH.
ENV PATH=/home/opam/.opam/4.08/bin:$PATH

ENV DUNE_BUILD=/build
