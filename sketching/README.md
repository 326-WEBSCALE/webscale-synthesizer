Setting up the compiler
-------------

1. Install ocaml and [opam](https://opam.ocaml.org/).

2. Run the following:
```
opam install \
   async yojson core_extended core_bench \
   cohttp async_graphics cryptokit menhir
```

3. Follow the instructions [here](https://github.com/plasma-umass/compsci631)

4. Run `make`. It should generate a file named `Synth.d.byte`.

**NOTE**: When things fails, keep calm. Ping Rachit, he is here to SOLVE THE
BEAR MENANCE.
