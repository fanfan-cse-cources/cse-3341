; author Yiqing Li (li.9073)
; This function check whether an element is in the list or not
; This function require element e and list l as the arguments
; This function will return true if e is in l, false otherwise
(define (elementCheck e l)
  (cond
    ((null? l) #f)
    ((eq? e (car l)) #t)
    (#t (elementCheck e (cdr l)))
  )
)

; This function eliminate elements that also in l2 from l1
; This function require three lists as arguments, result list are for return, l1 l2 are input lists
; This function will return a list of number has all elements in l1, except those in l2

(define (eliminates result l1 l2)
  (cond
    ((null? l1) result)
    ((elementCheck (car l1) l2) (eliminates result (cdr l1) l2))
    (#t (eliminates (cons (car l1) result) (cdr l1) l2)) 
  )
)

; This function finish elimination requirements
; This function require two lists l1, l2 as arguments
; This function will return a new list which has all elements in l1, except those in l2
(define (eliminate l1 l2)
  (eliminates '() l1 l2)
)

; This function get the maximum value from a list
; This function require an element m and a list l as arguments
; This function will return the maximum value from the list l
(define (getMax m l)
  (cond
    ((null? l) m)
    ((< m (car l)) (getMax (car l) (cdr l)))
    (#t (getMax m (cdr l)))
  )
)

; This function remove an element e from a list
; This function require an element e and a list l as arguments
; This function will return the list without element e
(define (remove e l)
  (cond
    ((null? l) '())
    ((eqv? e (car l)) (cdr l))
    (#t (cons (car l) (remove e (cdr l))))
  )
)

; This function will sort a list in non-decreasing order
; This function require two lists as arguments, lists result and l
; This function will return a list sorted in non-decreasing order
(define (sorts result l)
  (cond
    ((null? l) result)
    (#t (sorts (cons (getMax (car l) (cdr l)) result) (remove (getMax (car l) (cdr l)) l)))
  )
)

; This function finish sorting requirements
; This function require a list to be sorted 
; This function will return a list sorted in non-decresing order
(define (sort l)
  (sorts '() l))
;;;Sort part end;;;

; Main function
; The function will return a new list a new list which will have all the elements of L1, except those that appear in L2, and, further, this list will be sorted in non-decreasing order

(define (eliminateNsort l1 l2)
  (sort (eliminate l1 l2))
)