open Core

let bind (x : 'a option) (op : 'a -> 'b option) : 'b option =
  match x with
  | None -> None
  | Some a -> op a

let ( >>= ) = bind

let read_file file = In_channel.read_lines file

let depths = List.map ~f:int_of_string (read_file "day1.txt")

(** Print input *)
(** let () = List.iter ~f:(printf "%d ") depths ; print_string "\n" *)

let rec head = function
| [] -> []
| [_] -> []
| x :: t -> x :: head t

let zip (l1: 'a list) (l2: 'b list) = match List.zip l1 l2 with
  | Ok r -> Some r
  | Unequal_lengths -> None

let res d = match List.tl d with
  | None -> 0
  | Some t ->
      match List.zip t (head d) with
      | Unequal_lengths -> 0
      | Ok comb -> let isbig = List.map comb ~f:(fun (x, y) -> if x > y then 1 else 0) in
            match (List.reduce isbig ~f:(+)) with
              | Some r -> r
              | None -> 0

let () = print_string (string_of_int (res depths)) ; print_string "\n"

let sublist l i j = List.take (List.drop l i) (j-i)

let res2 =
  let len = List.length depths in
  let l1 = sublist depths 0 (len-2) in
  let l2 = sublist depths 1 (len-1) in
  let l3 = sublist depths 2 len in
  zip l1 l2 >>= fun l12 ->
  zip l12 l3 >>= fun l123 ->
  Some (res (List.map l123 ~f:(fun ((x, y), z) -> x + y + z)))


let () = match res2 with
  | Some x -> print_string (string_of_int x) ; print_string "\n"
  | None -> print_string "something is wrong\n"
