;(define (Fib n)
;  (fibber 1 0 n))
;(define (fibber x y n)
;  (if (= n 0) y
;  (fibber (+ x y) x (- n 1)))
;)

(define (Fib n)
  (fibber 0 1 (- n 1))
)
(define (fibber x y n)
  (cond
    ((= n 0) y)
    (#t (fibber y (+ x y) (- n 1)))
  )
)
