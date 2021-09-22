; Grabbed xmemb from the slides in the class
; x is an atom
; list is a list
; returns true if x is included in list
; requires that x is not null
(define (xmemb x list)   ; is x a member of list?
    (cond
		((null?  list)  #f)
		((eq?  x  (car  list)) #t)   ; quote list?
        (#t (xmemb x (cdr list) ) )
	)
)

;Returns the intersection of lists L1 and L2
;L1 is a list
;L2 is a list
;requires that L1 and L2 be lists
(define (intersected L1 L2)
	(cond
    	((null? L1) '()) ;if L1 or L2 are null, their intersection would be an empty set
		((null? L2) '())
    	((xmemb (car L1) L2) (cons (car L1) (intersected (cdr L1) L2))) ; if car of L1 is a member of L2, return
																		; a list where that car is set as the car to
																		; a list that is the intersection of everything
																		; beneath it
    	(#t (intersected (cdr L1) L2))) ;otherwise, get rid of the car
)

;Returns a list that has the contents L1 - L2
;L1 is a list
;L2 is a list
;requires that L1 and L2 are lists
(define (negated L1 L2)
	(cond
		((null? L1) '()) ; if L1 is null, return an empty set
	 	((null? L2) L1) ; if L2 is null, return L1
		((xmemb (car L1) L2) (negated (cdr L1) L2)) ; if car of L1 is a member of L2, return a list where that car is
													; removed
		(#t (cons (car L1) (negated (cdr L1) L2))) ; otherwise, attach that car to a list that has had negated run
												   ; beneath it
	)
)

; Returns the max value in L1
; L1 is a list
; x is an atom
; requires that x is not null
(define (getmax L1 x)
	(cond 
		((null? L1) x) ;if L1 is null, return x
	    ((> (car L1) x) (getmax (cdr L1) (car L1))) ; if the first element in L1 is greater than x, check that element
													; against the rest of L1
	    (#t (getmax (cdr L1) x)) ; otherwise, check x against the rest of L1
	)
)

;Returns a list with x removed from L1
; L1 is a list
; x is an atom
; requires that x is not null
(define (remove L1 x)
	(cond 
		((null? L1) '()) ;if L1 is an empty list, it return an empty list
    	((eqv? (car L1) x) (cdr L1)) ;if x is eqv to the car of L1, return a list without that car
    	(#t (cons (car L1) (remove (cdr L1) x))) ; otherwise, append that car onto a list that has had remove called
												 ; on it
  	)
)

; Selection sort, yikes
(define (sort L1)
	(cond
		((null? L1) '()) ;if L1 is null, return null
		(#t (cons (getmax L1 (car L1)) (sort (remove L1 (getmax L1 (car L1)))))) ;append the max element in L1 to a list
																				 ;that is L1 with that element removed
	)
)


(define (eliminateNsort L1 L2)
	(sort (negated L1 (intersected L1 L2))) ; Sort( L1 - (L1 && L2))
)