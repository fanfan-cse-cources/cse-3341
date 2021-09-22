(define (findMax L)
  (cond
    ; if the tail of the list is null return the list head
    ((null? (cdr L)) (car L))
    ; if list head is larger, return list header
    ((> (car L) (findMax (cdr L))) (car L))
    ; keep checking all other elements except the first
    (#t (findMax (cdr L)))
  )
)

(define (remove x L)
  (cond
    ; if L is null, return an empty list
    ((null? L) '())
    ; if x equal to first element of L
    ((eq? x (car L)) (cdr L))
    ; return the list without element x
    (#t (cons (car L) (remove x (cdr L))))
  )
)

(define (exist x L)
  (cond
    ; if L1 is null return false
    ((null? L) #f)
    ; check the first element
    ((eq? x (car L)) #t)
    ; keep checking all other elements except the first
    (#t (exist x (cdr L)))
  )
)

(define (intersection ret L1 L2)
  (cond
    ; if L1 is null return nothing
    ((null? L1) ret)
    ; if the first element of the list of L1 exist in L2,
    ; then keep tracking the rest of element in L1
    ((exist (car L1) L2) (intersection ret (cdr L1) L2))
    ; return the list of element of intersection
    (#t (intersection (cons (car L1) ret) (cdr L1) L2))
  )
)

(define (sort ret L)
  (cond
    ; if L1 is null return nothing
    ((null? L) ret)
    ; putting the max element at the beginning of the list
    ; and remove the max from current list
    ; repeating this process then we will have a sorted list
    (#t (sort (cons (findMax L) ret) (remove (findMax L) L)))
  )
)

(define (eliminateNsort L1 L2)
  ; return the intersection and sort it as a list
  (sort '() (intersection '() L1 L2))
)
