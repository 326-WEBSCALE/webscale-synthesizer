opts=-use-ocamlfind \
	-pkg core \
	-pkg compsci631 \
	-tag thread \
	-tag debug \
	-tag bin_annot \
	-tag short_paths \
	-cflags "-w A-4-33-40-41-42-43-34-44-27"  \
	-cflags -strict-sequence

all:
	ocamlbuild $(opts) Synth.d.byte

clean:
	ocamlbuild -clean

test: all
	./Synth.d.byte inline-test-runner dummy


	#-syntax camlp4o \
	#-pkg pa_ounit.syntax \
