open Core

let bind (x : 'a option) (op : 'a -> 'b option) : 'b option =
  match x with
  | None -> None
  | Some a -> op a

let ( >>= ) = bind

let deopt lst = 
  List.filter_map ~f:(fun x -> x) lst

let read_file file = In_channel.read_lines file

let moves =  
  let lines = read_file "day2.txt" in
  let optl = List.map lines ~f:(fun l -> let ws = Str.bounded_split (Str.regexp " ") l 2 in 
    List.nth ws 0 >>= fun f ->
    List.nth ws 1 >>= fun s ->
      Some (f, int_of_string s)) in
  deopt optl

let () = List.iter moves ~f:(fun (x, y) -> printf "[%s, %d]\n" x y)

let movepos ((x, y): int * int) ((mv, pw): string * int) = match mv with
| "forward" -> (x + pw, y)
| "down" -> (x, y + pw)
| "up" -> (x, y - pw)
| _ -> (x, y) ;;


let res = 
  let start = (0, 0) in
  let (x, y) = List.fold_left moves ~init:(start) ~f:(movepos) in
  x * y

let () = printf "Result: %d\n" res

let aimmoveops ((x, y, z): int * int * int) ((mv, pw): string * int) = match mv with
| "forward" -> (x + pw, y + z * pw, z)
| "down" -> (x, y, z + pw)
| "up" -> (x, y, z - pw)
| _ -> (x, y, z)

let res2 = 
  let start = (0, 0, 0) in
  let (x, y, _) = List.fold_left moves ~init:(start) ~f:(aimmoveops) in
  x * y

  let () = printf "Result 2: %d\n" res2