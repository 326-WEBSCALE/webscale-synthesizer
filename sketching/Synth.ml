open Smtlib
open Sketching
open Printf

type store = (string * term) list
let width = ref 4

let z3_path = "/usr/bin/z3"

let sketch_initial : store ref = ref []
let checker = ref (Some [])

let rec lookup (iden : 'a) (ablist : ('a * 'b )list) : 'b option =
  match ablist with
  | [] -> None
  | (a',b')::tl when (a' = iden) -> Some b'
  | _::tl -> lookup iden tl

let iden_to_string : (identifier * term) list -> store =
    List.map (fun (x,y) -> let Id s = x in (s,y))

let rec zip (lst1 : ('a * 'c) list) (lst2 : ('a * 'b) list) =
  (*let l1 = List.length lst1 and l2 = List.length lst2 in
  if l1 != l2 then
    failwith ("Cannot zip lists of unequal size: " ^ (string_of_int l1)
    ^ " and " ^ (string_of_int l2))
  else*)
    match lst1 with
    | [] -> []
    | (a,b)::tl ->
        match lookup a lst2 with
      | Some m -> (m,b)::(zip tl lst2)
      | None -> failwith ("Could not find association of var -- ZIP")

(* Updates a list with a association,
  - Adds association to list if first member not already present
  - Updates association with the second element if first element exists *)
let rec update_list (lst : ('a * 'b) list) (a : 'a) ( b : 'b) : ('a * 'b) list =
  match lst with
  | [] -> (a,b)::[]
  | (lst_a,lst_b)::tl when (a = lst_a) -> (lst_a,b)::tl
  | hd::tl -> hd::(update_list tl a b)

let rec store_to_string store : string =
  match store with
  | [] -> ""
  | (iden,_)::tl -> iden^"; "^(store_to_string tl)

module Initial_Store = struct

  let rec exp_is solver store exp : store =
  match exp with
  | EId id -> if (lookup id store = None) then
                let term_ = Id id in
                declare_const solver term_ (bv_sort !width);
                update_list store id (Smtlib.Const term_)
              else store
  | EOp1(_,e1) -> exp_is solver store e1
  | EOp2(_,e1,e2) -> let store' = exp_is solver store e1 in
                      exp_is solver store' e2
  | EInt _ | EWidth -> store
  | EHole loc ->
    let hole_id = "hole_" ^ (string_of_int loc) in
    declare_const solver (Id hole_id) (bv_sort !width);
    update_list store hole_id (Smtlib.const hole_id)

  let rec cmd_is solver store cmd : store =
  match cmd with
  | CAssign (id,exp) ->
      let store' = exp_is solver store exp in
      if (lookup id store' = None) then
        let term_ = Id id in
          declare_const solver term_ (bv_sort !width);
          update_list store' id (Smtlib.Const term_)
      else store'
  | CIf (pred,c1,c2) ->
      let store1 = exp_is solver store pred in
      let store2 = cmd_is solver store1 c1 in
      cmd_is solver store2 c2
  | CSeq (c1,c2) ->
      let store' = cmd_is solver store c1 in
      cmd_is solver store' c2
  | CSkip | CAbort -> store
  | CRepeat (id,e,c) ->
    let store1 = exp_is solver store e in
    let store2 = cmd_is solver store1 c in
    if(lookup id store2 = None) then
      let term_ = Id id in
          declare_const solver term_ (bv_sort !width);
          update_list store2 id (Smtlib.Const term_)
      else store2
end

let collect_and_declare_vars solver (cmd : cmd) : store =
    Initial_Store.cmd_is solver [] cmd

module To_Formula = struct

  let rec exp_tf (store : store) (exp : exp) : term =
      match exp with
      | EId x ->
        (match lookup x store with
        | None -> failwith (
          "Could not find association to " ^ x
          ^ " in store: " ^ store_to_string store^ " -- EXP_TO_FORMULA")
        | Some term_ -> (*print_endline ("Replacing "^ x);*)term_)
      | EInt i -> Smtlib.bv i !width
      | EWidth -> Smtlib.bv !width !width
      | EOp1(op,e) ->
        let t = exp_tf store e in
        (match op with
        | BNot -> bvnot t
        | LNot -> ite
          (equals t (Smtlib.bv 0 !width)) (bv 1 !width) (Smtlib.bv 0 !width) )
      | EOp2 (op,e1,e2) ->
        let t1 = exp_tf store e1 in
        let t2 = exp_tf store e2 in
       (match op with
        | Add -> bvadd t1 t2
        | Sub -> bvsub t1 t2
        | Mul -> bvmul t1 t2
        | Div -> bvudiv t1 t2
        | Mod -> bvsmod t1 t2
        | LShift -> bvshl t1 t2
        | RShift -> bvashr t1 t2
        | BAnd -> bvand t1 t2
        | BOr -> bvor t1 t2
        | LAnd -> ite (or_ (equals t1 (Smtlib.bv 0 !width)) (equals t2 (Smtlib.bv 0 !width))) (Smtlib.bv 0 !width) (bv 1 !width)
        | LOr -> ite (and_ (equals t1 (Smtlib.bv 0 !width)) (equals t2 (Smtlib.bv 0 !width))) (Smtlib.bv 0 !width) (bv 1 !width)
        | Eq -> ite (equals t1 t2) (bv 1 !width) (bv 0 !width))

      | EHole i ->
        let hole_id = ("hole_" ^ string_of_int i) in
        match lookup hole_id store with
        | None -> failwith ("Could not find term associated to " ^ hole_id
                             ^ " in store: " ^ store_to_string store^ " -- EXP_TO_FORMULA")
        | Some term_ -> term_

  let rec if_consolidate pred_term c_store a_store : store =
    match c_store with
    | [] -> []
    | (id,c_term)::tl ->
      match lookup id a_store with
      | None -> failwith ("Could not find " ^ id ^
                          " in the alternate store")
      | Some a_term ->
        let if_term = ite (not_ (equals pred_term (bv 0 !width))) c_term a_term in
        (if (a_term = c_term) then
          (id,c_term)
        else
          (id,if_term))::(if_consolidate pred_term tl a_store)

  let simp_loop_const store (formula : exp) : int =
    let simp_solver = make_solver z3_path in
    let loop_id = const "loop_const" in
      declare_const simp_solver (Id "loop_const") (bv_sort !width);
    let formula_t = exp_tf store formula in

    (try assert_ simp_solver (equals loop_id formula_t) with
      Failure msg -> failwith ("Failed to simply loop constant, there may be "^
                    "varibles which are not associated to a constant : "^msg));

    match check_sat simp_solver with
    | Unsat | Unknown -> failwith "Failed to simply loop constant"
    | Sat ->
      let simp_store = iden_to_string (get_model simp_solver) in
      let val_term =
      ( match lookup "loop_const" simp_store with
                       | None -> failwith "Failed to find loop constant in the simplified model"
                       | Some t -> t) in
      match val_term with
      | BitVec (i,_) -> i
      | _ -> failwith "Value returned by z3 not in simplest form (not possible)."

  let rec cmd_tf store cmd : store =
   (* print_endline ("Converting: " ^ (Sketching.to_string cmd) ^
                   "  Store: " ^ store_to_string store);*)
    match cmd with
    | CSkip | CAbort -> store
    | CAssign (id,exp) ->
      let assign_term = exp_tf store exp in
      update_list store id assign_term
    | CSeq (c1,c2) ->
      let store' = cmd_tf store c1 in
      cmd_tf store' c2
    | CIf (p,c,a) ->
      let pt = exp_tf store p in
      let c_store = cmd_tf store c and
          a_store = cmd_tf store a in
      if_consolidate pt c_store a_store
    | CRepeat (x,exp,c) ->
      let unroll_fac = (simp_loop_const store exp) in
      unroll_loop_tf store x c unroll_fac
      (*match exp with
      | EInt i -> unroll_loop_tf store x c i
      | EWidth -> unroll_loop_tf store x c !width
      | _ -> failwith "Loop must be repeated constant times -- CMD_TF"*)


  and unroll_loop_tf store id (c : cmd) (reps : int) : store  =
    let rec iterate store' (iter : int) : store =
    match iter with
    | n when (n=reps)-> store'
    | n ->
      let new_store = cmd_tf (update_list store' id (bv n !width)) c in
      iterate new_store (iter + 1)
    in
      List.filter (fun (x,y) -> (not (x = id))) (iterate store 0)
end

let cmd_to_store (store : store) (cmd : Sketching.cmd) : store =
  To_Formula.cmd_tf store cmd

module Cegis_Loop = struct
  let rec list_to_conjunction (lst : ('a * 'a ) list) : Smtlib.term =
    match lst with
    | [] -> failwith "Empty list passed -- LIST_TO_CONJUNCTION"
    | (t1,t2)::[] -> (equals t1 t2)
    | (t1,t2)::tl when t1 = t2 -> (list_to_conjunction tl)
    | (t1,t2)::tl -> and_ (equals t1 t2) (list_to_conjunction tl)

  let verif_and_model solver
    (store : (string * term) list)
    (spec : cmd)
    (sketch : cmd) : (identifier * term) list option =
    let spec_store = cmd_to_store store spec in
    let sketch_store = cmd_to_store store sketch in
    let (z_store : (term * term) list) = zip spec_store sketch_store in
    let conjunct = list_to_conjunction z_store in
        push solver;
        assert_ solver (not_ conjunct);
    match check_sat solver with
    | Sat -> let ret =  Some (get_model solver) in
              pop solver; checker := ret; ret
    | Unsat -> pop solver; None
    | Unknown -> failwith "Solver returned unknown, should not happen -- VERIF_AND_MODEL"

  let synth_val_gen solver store (spec : cmd) (sketch : cmd) =
    let spec_f = cmd_to_store store spec in
    let sketch_f = cmd_to_store store sketch in
    let (z_store : (term * term) list) = zip spec_f sketch_f in
    let conjunct = list_to_conjunction z_store in
        assert_ solver conjunct;
    match (check_sat solver) with
    | Sat -> get_model solver
    | _ -> failwith "Failed to generate values, spec and sketch not consistent -- SYNTH_VAL_GEN"

  let solver_ini (synth : solver) (verif : solver) spec sketch :
    (store * store) =
    let spec_initial = collect_and_declare_vars verif spec in
    let sketch_initial = collect_and_declare_vars synth sketch in
    (spec_initial, sketch_initial)

  let rec consolidate_stores o_store u_store =
    match u_store with
    | [] -> o_store
    | (a,b)::tl -> consolidate_stores (update_list o_store a b) tl

  let is_hole str : bool =
    (String.length str > 5) &&
    ((String.sub str 0 5) = "hole_")

  let filter_holes store : store =
    List.filter (fun (x,y) -> is_hole x) store

  let filter_no_holes store : store =
    List.filter (fun (x,y) -> not (is_hole x)) store

  let rec cegis_loop (hole_store : store) synth verif spec sketch : store =
    match (verif_and_model verif hole_store spec sketch) with
    | None -> hole_store
    | Some ex_store ->
      (* The example store is a assoc of ident and term, convert to store *)
      let const_vals = filter_no_holes (iden_to_string ex_store) in
      (* Remove all hole values from the store for synthesis system
          and consolidate with the inital sketch store *)
      let store_for_synth = consolidate_stores !sketch_initial const_vals in
      (* Synthesize values for the next iteration *)
      let synth_res = synth_val_gen synth store_for_synth spec sketch in
      (* The store is an assoc of ident and term, convert to store *)
      let hole_vals = filter_holes (iden_to_string synth_res) in
      (* Remove all non-hole values, consolidate with the initial spec store *)
      let store_for_verif = consolidate_stores hole_store hole_vals in
      (* Pass new store for the next iteration *)
      cegis_loop store_for_verif synth verif spec sketch
end

module Fill_Holes = struct
  let rec fill_exp store exp : exp =
    match exp with
    | EHole i ->
      let hole_id = ("hole_" ^ string_of_int i) in
      (match lookup hole_id store with
      | None -> failwith ("Could not find value for " ^ hole_id)
      | Some (BitVec (n,_)) -> EInt n
      | _ -> failwith (hole_id ^ " is not in a simplified form"))
    | EOp1(op,e) -> EOp1(op,fill_exp store e)
    | EOp2(op,e1,e2) -> EOp2(op,fill_exp store e1,fill_exp store e2)
    | _ -> exp

  let rec fill_cmd store cmd : cmd =
    match cmd with
    | CSkip | CAbort -> cmd
    | CAssign(i,e) -> CAssign (i,fill_exp store e)
    | CSeq(c1,c2) -> CSeq (fill_cmd store c1, fill_cmd store c2)
    | CIf (e,c1,c2) -> CIf(fill_exp store e, fill_cmd store c1, fill_cmd store c2)
    | CRepeat (i,e,c) -> CRepeat(i,fill_exp store e, fill_cmd store c)
end

let complete_sketch hole_store sketch =
  Fill_Holes.fill_cmd hole_store sketch

let cegis_simp (synth : solver) (verif : solver)
  (sketch : cmd) (spec : cmd) : Sketching.cmd option =
  let (spec_store,sketch_store) = Cegis_Loop.solver_ini synth verif spec sketch in
    (*spec_initial := spec_store;*)
    sketch_initial := sketch_store;
  let hole_val_guess =
   Cegis_Loop.consolidate_stores !sketch_initial
                      (List.map (fun (x,_) -> (x,(Smtlib.bv 1 !width)))
                                (Cegis_Loop.filter_holes !sketch_initial)) in
  let hole_store = Cegis_Loop.cegis_loop hole_val_guess synth verif spec sketch in
  Some (complete_sketch (Cegis_Loop.filter_holes hole_store) sketch)

module Sketch_loops = struct

  type guess_store = (string * int) list

  (* Remember to pad the list if an empty list is given
      - Corresponds to the case when sketch loops are not holes
  *)
  let rec gen_stream (store : (string * int) list) :
    (string * int) list list =
    let rec unfold (p : string * int) : (string * int) list =
        match p with
        | (s,n) when n>(!width+10) -> []
        | (s,n) -> (s,n)::(unfold (s,n+1))
    in
    let helper (p : string * int) store =
      List.map (fun (x : string * int) -> (x::[]) @ store) (unfold p)
    in
    match store with
    | [] -> []
    | p::[] -> List.map (fun x -> x::[]) (unfold p)
    | p::tl ->
      List.flatten (List.map (fun x -> helper p x) (gen_stream tl))

  let rec collect_loop_hole gstore cmd : guess_store =
  match cmd with
  | CRepeat (id,exp,_) ->
    ( match exp with
      | EHole i -> let lid = "loop_"^id in
          update_list gstore lid 1
      | _ -> gstore)
  | CSeq(c1,c2) | CIf(_,c1,c2) ->
    let gstore'= collect_loop_hole gstore c1 in
    collect_loop_hole gstore' c2
  | _ -> gstore


  let rec fill_loop_hole gstore cmd : cmd =
  match cmd with
  | CRepeat (id,exp,c) ->
    ( match exp with
      | EHole i ->
        let lid = "loop_"^id in
        (match lookup lid gstore with
        | Some guess -> CRepeat (id, EInt guess, c)
        | None -> failwith ("Could not find the value of " ^ lid ^ " in guess store"))
      | _ -> cmd)
  | CSeq(c1,c2) ->
    CSeq(fill_loop_hole gstore c1,
         fill_loop_hole gstore c2)
  | CIf(e,c1,c2) ->
    CIf(e,
        fill_loop_hole gstore c1,
        fill_loop_hole gstore c2)
  | _ -> cmd

  let rec gsstring store =
  match store with
  | [] -> ""
  | (i,n)::tl -> (i ^ "," ^ (string_of_int n)^ "; ")^(gsstring tl)

  let guess_check (gstore : guess_store) (synth : solver)
    (verif : solver)  (sketch : cmd) (spec : cmd): cmd option =
  let no_loop_sketch = fill_loop_hole gstore sketch in
  (*print_endline ("Converting: " ^ (Sketching.to_string no_loop_sketch));*)
  try (cegis_simp synth verif no_loop_sketch spec) with
  Failure msg ->
    (*print_endline (Sketching.to_string no_loop_sketch);
    print_endline msg;*)
    None


  let rec guess_loop (guess_stream : guess_store list)
    (sketch : cmd) (spec : cmd) : cmd option =
  let synth = Smtlib.make_solver z3_path in
  let verif = Smtlib.make_solver z3_path in
  match guess_stream with
  | [] -> None
  | gstore::tl ->
    (*print_endline ("\n");
    print_endline (gsstring gstore);*)
    ( match guess_check gstore synth verif sketch spec with
      |(Some c) as sol -> sol
      | None -> guess_loop tl sketch spec)

  let sketch_guess_loop (sketch : cmd) (spec : cmd) : cmd option =
  let ini = collect_loop_hole [] sketch in
  let gstore_stream : (guess_store list) = gen_stream ini in
  match gstore_stream with
  | [] ->
    let synth = Smtlib.make_solver z3_path in
    let verif = Smtlib.make_solver z3_path in
    (cegis_simp synth verif sketch spec)
  | _ -> guess_loop gstore_stream sketch spec
end

let cegis (w : int) (synth : solver) (verif : solver)
  (sketch : cmd) (spec : cmd) : Sketching.cmd option =
  width := w;
  Sketch_loops.sketch_guess_loop sketch spec

let _ =
  let synth = Smtlib.make_solver z3_path in
  let verif = Smtlib.make_solver z3_path in
  let w = int_of_string Sys.argv.(1) in
      width := w;
  let sketch = Sketching.from_file Sys.argv.(2) in
  let spec = Sketching.from_file Sys.argv.(3) in
  match cegis (!width) synth verif sketch spec with
    | None -> (printf "Synthesis failed.\n%!"; exit 1)
    | Some sketch' ->
      print_endline (Sketching.to_string sketch')
